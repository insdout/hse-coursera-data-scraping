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
    # your code here
    return # your code here


def get_movie_distance(actor_start_url, actor_end_url,
        num_of_actors_limit=None, num_of_movies_limit=None):
    # your code here
    return # your code here


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # your code here
    return # your code here
