from utils.my_functions import *
import folium
import sqlalchemy



class User:
    def __str__(self) -> str:
        return f'Użytkownik {self.nick} z {self.location} ma {self.posts} postów'
    
    def __init__(self, id, connection):
        self.id = id
        self.nick = self.get_user_nick(connection)
        self.name = self.get_user_name(connection)
        self.age = self.get_user_age(connection)
        self.posts = self.get_user_posts(connection)
        self.location = self.get_user_location(connection)
    
    def get_user_nick(self,connection):
        result = connection.execute(sqlalchemy.text(f"SELECT nick FROM mytable WHERE id = '{self.id}'"))
        return alchemy_1dcursor_to_string(result)
    
    def get_user_name(self,connection):
        result = connection.execute(sqlalchemy.text(f"SELECT name FROM mytable WHERE id = '{self.id}'"))
        return alchemy_1dcursor_to_string(result)
        
    def get_user_age(self,connection):
        result = connection.execute(sqlalchemy.text(f"SELECT age FROM mytable WHERE id = '{self.id}'"))
        return int(alchemy_1dcursor_to_string(result))

    def get_user_posts(self,connection):
        result = connection.execute(sqlalchemy.text(f"SELECT posts FROM mytable WHERE id = '{self.id}'"))
        return int(alchemy_1dcursor_to_string(result))
    
    def get_user_location(self,connection):
        result = connection.execute(sqlalchemy.text(f"SELECT location FROM mytable WHERE id = '{self.id}'"))
        return alchemy_1dcursor_to_string(result)
    
            
    def get_weather_for_city(self):
        formated_city = self.location.replace(" ", "").lower().strip()
        url_weather = f"https://danepubliczne.imgw.pl/api/data/synop/station/{formated_city}"
        return requests.get(url=url_weather).json()
    
    
    def __get_map__(self):
        get_map_of_one_user(self.location,self.nick).open_in_browser()
        
u1 = User("Jan Kowalski","jankowalski",10,"Warszawa")
print(u1.get_weather_for_city())