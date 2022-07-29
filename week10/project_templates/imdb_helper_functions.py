from bs4 import BeautifulSoup
import time
import requests
import urllib


def get_soup_movies_by_actor(actor_url):
    url = "https://www.imdb.com/name/"
    url_to_pass = urllib.parse.urljoin(url, actor_url)
    headers = {'Accept-Language': 'en',
               'X-FORWARDED-FOR': '2.21.184.0'}

    response = requests.get(url_to_pass, headers=headers)
    print(response.status_code)
    #print(url_to_pass)
    assert response.status_code == 200, "Wrong response code: {}".format(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_soup_actors_by_movie(movie_url):
    url = "https://www.imdb.com/title/"
    url_to_pass = urllib.parse.urljoin(url, movie_url) + "fullcredits/"
    headers = {'Accept-Language': 'en',
               'X-FORWARDED-FOR': '2.21.184.0'}

    response = requests.get(url_to_pass, headers=headers)
    print(response.status_code)
    #print(url_to_pass)
    assert response.status_code == 200, "Wrong response code: {}".format(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup



