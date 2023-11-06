from utils.my_functions import *


load_data()
is_exit = False       
while (is_exit == False):
    command = input("Enter command: ").split(" ")
    match command[0]:
        case "exit": is_exit = True
        case "create":
            if len(command) == 4: create_user(command[1],command[2],command[3])
            elif len(command) == 3: create_user(command[1],command[2])
            else: create_user()
            
        case "delete":
            if len(command) < 2: 
                delete_user()
            else: delete_user(command[1])
        case "update":
            if len(command) == 3: update_user(command[1],command[2])
            else: update_user()
            update_user(command[1],command[2],command[3])
        case "list": list_all_users()
        case "save": save_data()
        case "help": help_command()
        case _: print("Unknown command, try help")

    