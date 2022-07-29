# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
from imdb_helper_functions import get_soup_movies_by_actor, get_soup_actors_by_movie
from bs4 import BeautifulSoup
import time
import requests
import urllib
from collections import deque
import pickle

with open('movie_to_actors.pkl', 'rb') as f:
    movie_to_actors = pickle.load(f)
with open('actor_to_films.pkl', 'rb') as f:
    actor_to_films = pickle.load(f)


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    actors_list = []
    cast_list = cast_page_soup.find('table', class_='cast_list')
    actors = cast_list.find_all('td', class_='')
    for actor in actors[0:num_of_actors_limit]:
        actors_list.append(tuple((actor.find('a').text.strip(),
                                  urllib.parse.urljoin(
                                      "https://www.imdb.com/",
                                      actor.find('a')['href'])
                                  )))
        # print(actor.find('a').text.strip(), urllib.parse.urljoin(url,actor.find('a')['href']))
    return actors_list


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):
    filmograpy = actor_page_soup.find('div', class_='filmo-category-section')
    films_all = filmograpy.find_all('div', attrs={"class": ["filmo-row odd", "filmo-row even"]})
    films_list = []
    counter = 0
    for film in films_all:
        film_name = film.find("a").text.strip()
        film_link = film.find("a")["href"].strip()
        film_year = film.find("span", class_="year_column").text.strip()
        film_notes = film.find("b").next_sibling.strip()
        if not film_notes and film_year:
            counter += 1
            if num_of_movies_limit:
                if counter >= num_of_movies_limit:
                    break
            films_list.append(tuple((film_name,
                                     urllib.parse.urljoin(
                                         "https://www.imdb.com/",
                                         film_link))))
            # print("APPENDED-> name:", film_name, "link:", film_link, "year:", film_year, "notes:", film_notes)
        # print("name:", film_name, "link:", film_link, "year:", film_year, "notes:", film_notes)
    return films_list


def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None):

    stop = 0
    v_actors = set(actor_start_url)
    q = deque()
    q.append((actor_start_url, 0))
    print("q", q)
    while deque and stop <= 1000:
        stop += 1
        v = q.popleft()
        print("vertice:", v)
        if v not in v_actors:
            dist = v[1]
            url = v[0]
            print("url:", url, "dist:", dist)
            if dist >= 10:
                return None
            if url == actor_end_url:
                return dist
            edges = list(map(lambda x: x[1], get_dist1_people_by_actor(url)))
            for edge in edges:
                if edge not in v_actors:
                    q.append((edge, dist+1))
                #print("q_append:", q)
                    v_actors.add(url)


def get_dist1_people_by_actor(actor_url):
    dist1_people = []
    print("asked for:", actor_url)
    if actor_url in actor_to_films:
        movies_list = actor_to_films.get(actor_url)
        #print("found actor", actor_url, movies_list)
    else:
        movies_list = get_movies_by_actor_soup(get_soup_movies_by_actor(actor_url))
        actor_to_films[actor_url] = movies_list
        with open('actor_to_films.pkl', 'wb') as f:
            pickle.dump(actor_to_films, f)
        #print("added:", actor_to_films)
    for movie in movies_list:
        #print("movie:", movie)
        if movie in movie_to_actors:
            dist1_people.extend(movie_to_actors.get(movie))
            #print("found movie", movie, movie_to_actors.get(movie))
        else:
            m = get_actors_by_movie_soup(get_soup_actors_by_movie(movie[1]))
            dist1_people.extend(m)
            movie_to_actors[movie] = m
            with open('movie_to_actors.pkl', 'wb') as f:
                pickle.dump(movie_to_actors, f)
            #print("added movie:", movie, m)
        #print(dist1_people)
    return dist1_people

def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # your code here
    return # your code here




if __name__ == "__main__":
    url_start = "https://www.imdb.com/name/nm0000237/"
    url_end = "https://www.imdb.com/name/nm0000138/"
    print(get_movie_distance(url_start, url_end,
                       num_of_actors_limit=None, num_of_movies_limit=None))

