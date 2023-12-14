from utils.my_functions import *
import folium
import sqlalchemy
class User:
    def __init__(self, nick, connection):
        self.nick = nick
        self.name = get_user_name(connection)
        self.age = get_user_age(connection)
        

        
    def __str__(self) -> str:
        return f'Użytkownik {self.nick} z {self.residence} ma {self.posts} postów'
    
    
    def __update__(self,to_change:list[str]):
        if to_change[0] != None:
            self.name = to_change[0]
        if to_change[1] != None:
            self.nick = to_change[2]    
        if to_change[2] != None:
            self.posts = to_change[1]
            
    def get_weather_for_city(self):
        formated_city = self.residence.replace(" ", "").lower().strip()
        url_weather = f"https://danepubliczne.imgw.pl/api/data/synop/station/{formated_city}"
        return requests.get(url=url_weather).json()
    
    
    def __get_map__(self):
        get_map_of_one_user(self.residence,self.nick).open_in_browser()
        
u1 = User("Jan Kowalski","jankowalski",10,"Warszawa")
print(u1.get_weather_for_city())