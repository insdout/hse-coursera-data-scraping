# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
from imdb_helper_functions import helper_function_example



def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    actors_list = []
    cast_list = cast_page_soup.find('table', class_='cast_list')
    actors = cast_list.find_all('td', class_='')
    for actor in actors[0:num_of_actors_limit]:
        actors_list.append(tuple((actor.find('a').text.strip(), actor.find('a')['href'])))
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
            films_list.append(tuple((film_name, film_link)))
            # print("APPENDED-> name:", film_name, "link:", film_link, "year:", film_year, "notes:", film_notes)
        # print("name:", film_name, "link:", film_link, "year:", film_year, "notes:", film_notes)
    return films_list


def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None):
    # your code here
    return # your code here


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # your code here
    return # your code here
