import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
a = load_dotenv()


db_params = sqlalchemy.engine.URL.create(
    drivername='postgresql',
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"))

engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
sql_query_1 = sqlalchemy.text("SELECT name FROM mytable WHERE name = 'Kowalczyk'")
result = connection.execute(sql_query_1)
result = [r for r in result]
for character in result:
    var = (character[0])
print (var)


# TODO: Add to actual code datebase connection and functions to add, delete, update and list users
# TODO: Add table to database with users data
# TODO: Rewrite to object oriented code
# TODO: Sprawozdanie (strona tytułowa, spis treści, opis kodu realizującego zadanie rysowania mapy uwzględniającego opis funkcji, podsumowanie, wnioski końcowe)


def get_coordinates_of(city:str)->list[float,float]:
    """
    Retrieves the latitude and longitude coordinates of a given city.

    Args:
        city (str): The name of the city.

    Returns:
        list[float, float]: A list containing the latitude and longitude coordinates.
    """
    adress_url = f'https://pl.wikipedia.org/wiki/{city}'
    response = requests.get(url=adress_url)
    latitude = float(BeautifulSoup(response.text, 'html.parser').find_all('span', class_='latitude')[1].text.replace(',', '.')) # .latitude is same as class_='latitude'
    longitude = float(BeautifulSoup(response.text, 'html.parser').select('.longitude')[1].text.replace(',','.')) # .longitude is same as class_='longitude' 
    return [latitude,longitude]    
      
def generate_map_for_user() -> None:
    """
    Prompts the user to enter a city name and prints the coordinates of the city.
    """
    nick = input("Enter user nick: ")
    city = ""
    for user in user_data:
        if user["nick"] == nick:
            city = user["city"]
    if city != "":
        get_map_of_one_user(city,nick).save(f'{nick}_mapka.html')
    
def get_map_of_one_user(city:str,user_name:str)->None:
    map = folium.Map(location=get_coordinates_of(city),
                 tiles="OpenStreetMap", 
                 zoom_start=6)
    folium.Marker(location=get_coordinates_of(city),
                  popup=f'Tu mieszka {user_name}').add_to(map) 
    return map 

def generate_map_of_all_users():
    map = folium.Map(location=[53, 19.0], zoom_start=6)
    for user in user_data:
        folium.Marker(location=get_coordinates_of(user["city"]),
                  popup=f'Tu mieszka {user["nick"]}').add_to(map)
    map.save("all_users.html")
    
def get_weather_for_city(name_of_city: str):
    """
    Retrieves weather information for a given city.

    Args:
        name_of_city (str): The name of the city.

    Returns:
        dict: A dictionary containing weather information for the city.
    """
    formated_city = name_of_city.replace(" ", "").lower().strip()
    url_weather = f"https://danepubliczne.imgw.pl/api/data/synop/station/{formated_city}"
    return requests.get(url=url_weather).json()