
class User:
    def __init__(self,name, nick, posts):
        self.name = name
        self.posts = posts
        self.nick = nick
        
    def __str__(self) -> str:
        return f'Użytkownik {self.nick} ma {self.posts} postów'
    
    def __update__(self,to_change:list[str]):
        if to_change[0] != None:
            self.name = to_change[0]
        if to_change[1] != None:
            self.nick = to_change[2]    
        if to_change[2] != None:
            self.posts = to_change[1]

all_users_list:list[User] = []
isExit = False


def add_user():
    new_name = input("Enter name: ")
    new_nick = input("Enter nick: ")
    new_posts = input("Enter age: ")
    all_users_list.append(User(new_name,new_nick,new_posts))

while (isExit != True):
    user_input = input("Enter command: ")
    if (user_input == "exit"):
        isExit = True
    elif (user_input == "add"):
        add_user()
    elif (user_input == "list"):
        for user in all_users_list:
            print(user.__str__())
    else:
        print("Unknown commend")

#print(f'To jest facebook {user_data[0]["nick"]}!!!!')
#print(f'To jest facebook {all_users_list[0].nick} i ma {all_users_list[0].age} lat!!!!')
