import orm.dml as dml
import requests
from bs4 import BeautifulSoup
import folium

is_exit = False
engine = None

def main():
    init_database_and_connection()
    while is_exit == False:
        display_menu()
    print("Zamykam program")

def exit():
    global is_exit
    is_exit = True
    engine.dispose()


def init_database_and_connection():
    """
    Initializes the database connection and checks if the connection is successful.

    Raises:
        Exception: If the connection to the database fails.

    Returns:
        None
    """
    global engine
    try:
        engine = dml.create_engine()
        try_con = engine.connect()
        try_con.close()
        print("Nawiązano połączenie z bazą danych")
    except Exception: 
        print("Nie udało się nawiązać połączenia z bazą danych")
        exit()
        return
    dml.create_table(engine)

def display_menu():
    print(f'Menu:\n'
            f'1. Dodaj użytkownika\n'
            f'2. Usuń użytkownika\n'
            f'3. Zaktualizuj użytkownika\n'
            f'4. Lista wszystkich użytkowników\n'
            f'5. Stwórz mapę dla użytkownika/ów\n'
            f'6. Podaj pogodę dla użytkownika\n'
            f'0. Wyjdź\n')
    choice = input("Podaj numer opcji: ").strip()
    match choice:
        case "1":
            add_user()
        case "2":
            delete_user()
        case "3":
            update_user()
        case "4":
            list_users()
        case "5":
            option_generate_map()
        case "6":
            get_weather_for_user()
        case "0":
            exit()
        case "reset":
            dml.reset_table(engine)
        case _:
            print("Wybór może być tylko z zakresu 0-6")

def add_user():
    """
    Adds a new user to the system.

    Prompts the user to enter the user's name, nick, city, and number of posts.
    Checks if the nick is unique and prompts the user to enter a different nick if it is already taken.
    If the number of posts is not an integer, prompts the user to enter a valid integer.
    Calls function to add the user into the database.
    """
    global engine
    with dml.create_session(engine) as session:
        name = input("Wprowadż imię: ")
        while True:
            nick = input("Wprowadź nick: ")
            if dml.is_unique_nick(session,nick):
                break
            else:
                print("Nick jest już w bazie danych. Wpisz unikalną wartość.")
        city = input("Wpisz miasto użytkownika: ")
        while True:
            try:
                posts = int(input("Wpisz liczbę postów: "))
                break
            except ValueError:
                print("Liczba postów musi być liczbą całkowitą.")
        dml.create_user(session,nick,name,posts,city)

def delete_user():
    """
    Deletes a user from the database.

    This function prompts the user to enter the user's nickname, searches for the user in the database,
    and deletes the user if found. If the user is not found, it prints a message and returns.

    Parameters:
    None

    Returns:
    None
    """
    global engine
    with dml.create_session(engine) as session:
        nick = input("Wpisz nick użytkownika do usunięcia: ").strip()
        user = dml.user_from_nick(session,nick)
        if user is None:
            print("Nieznaleziono użytkownika o podanym nicku.")
            return
        session.delete(user)
        session.commit()

def update_user():
    """
    Updates the information of a user in the database.

    Prompts the user to enter the user's nick, name, city, and number of posts.
    If the user is found in the database, their information is updated accordingly.
    If the user is not found, a message is printed and the function returns.

    Parameters:
    None

    Returns:
    None
    """
    global engine
    with dml.create_session(engine) as session:
        nick = input("Wpisz nick użytkownika: ").strip()
        user = dml.user_from_nick(session,nick)
        if user is None:
            print("Użytkownik o podanym nicku nie istnieje.")
            return
        name = input("Wpisz imię użytkownika: ")
        city = input("Wpisz miasto użytkownika: ")
        while True:
            try:
                posts = input("Wpisz liczbę postów: ")
                if posts == "":
                    break
                posts = int(posts)
                break
            except ValueError:
                print("Liczba postów musi być liczbą całkowitą.")
        if name == "":
            name = user.name
        if city == "":
            city = user.city
        if posts == "":
            posts = user.posts
        try:
            user.name = name
            user.city = city
            user.posts = posts
            session.commit()
        except:
            session.rollback()
            print("Błąd przy aktualizacji użytkownika. Czy struktura tabeli jest poprawna?\nSpróbuj wykonać reset bazy danych komendą 'reset' w menu.")
        
def list_users():
    """
    Prints a list of all users with their information.
    """
    global engine
    with dml.create_session(engine) as session:
        try:
            users = session.query(dml.User).all()
        except:
            print("Błąd przy wyświetlaniu użytkowników. Czy struktura tabeli jest poprawna?.\nSpróbuj wykonać reset bazy danych komendą 'reset' w menu.")
            return
        if users == None or len(users) == 0:
            print("Brak użytkowników w bazie danych\n")
            return
        print("Lista wszystkich użytkowników:")
        for user in users:
                oneHalf = f'{user.id} | {user.nick}'.ljust(20)
                print(f'{oneHalf}| {user.name} ma {user.posts} postów i pochodzi z {user.city}')
            

def option_generate_map():
    """
    Prompts the user to choose whether to generate a map for a single user or for all users.
    """
    print("1. Wygeneruj mapę dla jednego użytkownika\n"
          "2. Wygeneruj mapę dla wszystkich użytkowników\n"
          "0. Powrót do menu głównego\n")
    choice = input("Podaj numer opcji: ").strip()
    match choice:
        case "1":
            generate_map_for_user()
        case "2":
            generate_map_of_all_users()
        case "0":
            return
        case _:
            print("Wybór może być tylko z zakresu 0-2")


def generate_map_for_user() -> None:
    """
    Generates a map for a user based on their city and nickname.
    Prompts the user to enter their nickname, retrieves the user's information from the database,
    and generates a map using the user's city and nickname. The generated map is saved as an HTML file.
    """
    global engine
    with dml.create_session(engine) as session:
        nick = input("Wpisz nick użytkownika do wygenerowania mapy: ").strip()
        user = dml.user_from_nick(session, nick)
        if user is None:
            print("Użytkownik o podanym nicku nie istnieje.")
            return
        get_map_of_one_user(user.city, user.nick).save(f'{user.nick}_mapka.html')
    
def get_map_of_one_user(city:str,user_name:str)->folium.Map:
    """
    Generates a folium map centered around a given city and adds a marker for a user.

    Parameters:
    city (str): The name of the city.
    user_name (str): The name of the user.

    Returns:
    folium.Map: A folium map object.
    """
    map = folium.Map(location=get_coordinates_of_location(city),
                 tiles="OpenStreetMap", 
                 zoom_start=9)
    folium.Marker(location=get_coordinates_of_location(city),
                  popup=f'Tu mieszka {user_name}').add_to(map) 
    return map


def generate_map_of_all_users():
    """
    Generates a map of all users' locations and saves it as an HTML file.

    Returns:
        None
    """
    global engine
    with dml.create_session(engine) as session:
        map = folium.Map(location=[53, 19.0], tiles='OpenStreetMap', zoom_start=7)
        all_users = session.query(dml.User).all()
        for user in all_users:
            location = get_coordinates_of_location(user.city)
            if location[0] is None:
                continue
            folium.Marker(location=location,
                          popup=f'Tu mieszka {user.name} ({user.nick})').add_to(map)
        map.save("all_users_map.html")

def get_coordinates_of_location(location: str) -> list[float, float]:
    """
    Retrieves the latitude and longitude coordinates of a given location.

    Args:
        location (str): The name of the location.

    Returns:
        list[float, float]: A list containing the latitude and longitude coordinates of the location.
                            If the coordinates cannot be found, [None, None] is returned.
    """
    formatted_location = location.replace(" ", "_")
    adress_url = f'https://pl.wikipedia.org/wiki/{formatted_location}'
    response = requests.get(url=adress_url)
    try:
        latitude = float(BeautifulSoup(response.text, 'html.parser').find_all('span', class_='latitude')[1].text.replace(',', '.'))
        longitude = float(BeautifulSoup(response.text, 'html.parser').select('.longitude')[1].text.replace(',', '.'))
    except IndexError:
        return [None, None]
    return [latitude, longitude]

def get_weather_for_user()->None:
    """
    Retrieves weather information for a user's city.

    This function prompts the user to enter their nickname, retrieves the user's city from the database,
    and then fetches the weather data for that city from an API. The weather information is then printed
    to the console.

    Raises:
        KeyError: If the weather data for the user's city is not available.

    Returns:
        None
    """
    global engine
    with dml.create_session(engine) as session:
        nick = input("Wpisz nick użytkownika do uzyskania pogody: ").strip()
        user = dml.user_from_nick(session,nick)
        if user is None:
            print("Użytkownik o podanym nicku nie istnieje.")
            return
        formated_city = format_city_for_weather(user.city)
        url_weather = f"https://danepubliczne.imgw.pl/api/data/synop/station/{formated_city}"        
        weather_dict =  requests.get(url=url_weather).json()
        try:
            print(f'Pogoda dla {user.city}: {weather_dict["temperatura"]}°C, {weather_dict["cisnienie"]}hPa, {weather_dict["wilgotnosc_wzgledna"]}% wilgotności względnej, {weather_dict["suma_opadu"]}mm suma opadów. Wiatr {weather_dict["kierunek_wiatru"]} z prędkością {weather_dict["predkosc_wiatru"]}m/s ')
        except KeyError:
            print(f"Brak pogody dla {user.city}")
            
def format_city_for_weather(city:str)->str:
    """
    Formats the city name for weather API by removing spaces, converting to lowercase, and replacing Polish characters with their ASCII equivalents.

    Args:
        city (str): The name of the city.

    Returns:
        str: The formatted city name.
    """
    polskie_znaki_dict = {"ą":"a","ć":"c","ę":"e","ł":"l","ń":"n","ó":"o","ś":"s","ź":"z","ż":"z"} 
    return ''.join(polskie_znaki_dict.get(char, char) for char in city.replace(" ", "").lower())


