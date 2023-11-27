from bs4 import BeautifulSoup
import requests


def get_coordinates_of(city:str)->list[float,float]:
    adress_url = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adress_url)
    latitude = float(BeautifulSoup(response.text, 'html.parser').find_all('span', class_='latitude')[1].text.replace(',', '.')) # .latitude is same as class_='latitude'
    longitude = float(BeautifulSoup(response.text, 'html.parser').select('.longitude')[1].text.replace(',','.')) # .longitude is same as class_='longitude' 
    return [latitude,longitude]
