from bs4 import BeautifulSoup
import requests
import folium
from orm.dml import *


def display_menu():
    print(f'Menu:\n'
            f'1. Add user\n'
            f'2. Delete user\n'
            f'3. Update user\n'
            f'4. List all users\n'
            f'5. Generate map for all users\n'
            f'6. Get weather for user place of living\n'
            f'0. Exit\n')
    choice = input("Enter your choice: ").strip()
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
            generate_map_of_all_users()
        case "6":
            get_weather_for_user()
        case "0":
            exit()
        case _:
            print("not a walid choice. enter a number from 0 to 6")

def add_user():
    with create_session(create_engine()) as session:
        name = input("Enter user name: ")
        while True:
            nick = input("Enter user nick: ")
            if is_unique_nick(session,nick):
                break
            else:
                print("Nick is already taken. Try something else.")
        city = input("Enter user city: ")
        while True:
            try:
                posts = int(input("Enter user posts: "))
                break
            except ValueError:
                print("Number of posts must be a intiger.")
        create_user(session,nick,name,posts,city)    

def delete_user():
    return None

def update_user():
    return None

def list_users():
    return None

def generate_map_of_all_users():
    return None

def get_weather_for_user():
    return None


