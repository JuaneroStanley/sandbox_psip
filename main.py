from Data import user_data
class User:
    def __init__(self,name, age, nick):
        self.name = name
        self.age = age 
        self.nick = nick

all_users_list:list[User] = []
isExit = False

for user in user_data:
    print(f'Your friend {user["nick"]} shared {user["posts"]} posts')


def add_user():
    new_name = input("Enter name: ")
    new_nick = input("Enter nick: ")
    new_age = input("Enter age: ")
    all_users_list.append(User(new_name,new_age,new_nick))

while (isExit != True):
    user_input = input("Enter commend: ")
    if (user_input == "exit"):
        isExit = True
    elif (user_input == "add"):
        add_user()
    elif (user_input == "list"):
        for user in all_users_list:
            print(f'Użytkownik {user.nick} ma {user.age} lat')
    else:
        print("Unknown commend")

#print(f'To jest facebook {user_data[0]["nick"]}!!!!')
#print(f'To jest facebook {all_users_list[0].nick} i ma {all_users_list[0].age} lat!!!!')

