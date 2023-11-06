user_data: list[str,str,int] =[]

def load_data() -> None:
    """
    Load data from a text file and store it in a list of dictionaries.
    Args: 
        None
    Returns:
        None
    """
    print(f'Loading data from database')
    file = open("sandbox_psip\data_text.txt","r",encoding="utf-8")
    x = 0
    for line in file:
        split_line = line[:-1].split(" ")
        user_data.append({"name":split_line[0],"nick":split_line[1],"posts":split_line[2]})
        x += 1
    print(f'Loaded {x} users')
    
    
def create_user(name:str = None, nick:str = None, posts:int = None)->None:
    """
    Creates a new user with the given name, nickname, and number of posts.

    If no arguments are provided, prompts the user to enter the information.

    Args:
        name (str, optional): The name of the user. Defaults to None.
        nick (str, optional): The nickname of the user. Defaults to None.
        posts (int, optional): The number of posts the user has made. Defaults to None.

    Returns:
        None
    """
    if name == None and nick == None and posts == None:
        name = input("Enter name: ")
        nick = input("Enter nick: ")
        posts = input("Enter posts: ")
    user_data.append({"name":name,"nick":nick,"posts":posts})
    print(f'User {nick} created')
    
def delete_user(nick:str = None)->None:
    """
    Deletes a user from the user_data list based on their nickname.

    Args:
        nick (str): The nickname of the user to be deleted. If None, the user will be prompted to enter a nickname.

    Returns:
    None
    """
    if nick == None:
        nick = input("Enter nick: ")
    users_to_delete = []
    for user in user_data:
        if user["nick"] == nick:
            users_to_delete.append(user)
    if len(users_to_delete) == 0:
        print(f'User {nick} not found')
    elif len(users_to_delete) == 1:
        user_data.remove(users_to_delete[0])
        print(f'User {nick} deleted')
    else:
        print(f'Found {len(users_to_delete)} users with nick {nick}')
        print(f'0. delete all')
        for x in range(len(users_to_delete)):
            print(f'{x+1}. User {users_to_delete[x]["name"]} has {users_to_delete[x]["posts"]} posts')
        id_delete = input("Enter id of user to delete: ")
        if (id_delete == "0"):
            for user in users_to_delete:
                user_data.remove(user)
            print(f'All users with nick {nick} deleted')
        else: 
            user_data.remove(users_to_delete[int(id_delete)-1])
            print(f'User {nick} deleted')
        
         
def update_user(nick:str = None, name:str = None, posts:int = None)->None:
    """
    Updates user data in the user_data list.
    
    Parameters:
        nick (str): Nickname of the user to be updated.
        name (str): New name of the user.
        posts (int): New number of posts of the user.
    
    Returns:
        None
        
    If no parameters are provided, the function prompts the user to enter them.
    """
    
    if nick == None and name == None and posts == None:
        nick = input("Enter nick: ")
        name = input("Enter name: ")
        posts = input("Enter posts: ")
    for user in user_data:
        if user["nick"] == nick:
            if name != None:
                user["name"] = name
            if posts != None:
                user["posts"] = posts
            print(f'User {nick} updated')
            
def list_all_users() -> None:
    """
    Prints a list of all users and their number of posts.
    """
    print(f'List of all users:')
    for user in user_data:
        print(f'User {user["nick"]} has {user["posts"]} posts')

def save_data() -> None:
    """
    Saves user data to a text file.

    The function opens a file named 'data_text.txt' and writes the name, nickname, and number of posts for each user in the user_data list.
    """
    
    print(f'Saving data to database')
    file = open("sandbox_psip\data_text.txt","w",encoding="utf-8")
    for user in user_data:
        file.write(f'{user["name"]} {user["nick"]} {user["posts"]}\n')
    print(f'Saved {len(user_data)} users')
    
    
def help_command() -> None:
    """
    Prints a list of available commands and their usage instructions.
    """
    print(f'Commands: create, delete, update, list, save, exit, ui')
    print(f'create - create new user can be used with 3 arguments: name, nick, posts')
    print(f'delete - delete user can be used with 1 argument: nick')
    print(f'update - update user can be used with 3 arguments: nick, name, posts')
    print(f'list - list all users')
    print(f'save - save data to database')
    print(f'ui - run user interface')
    print(f'exit - exit program')
    print(f'if you want to use command with arguments use space to separate them else you will need to enter them later in program')


def ui():
    ui_exit = False
    while (ui_exit == False):
        print(f'\nMenu:\n'
            f'0. Exit\n'
            f'1. Create user\n'
            f'2. Delete user\n'
            f'3. Update user\n'
            f'4. List all users\n'
            f'5. Save data to file\n'
          )
        match input("Enter function to run: "):
            case "1": create_user()
            case "2": delete_user()
            case "3": update_user()
            case "4": list_all_users()
            case "5": save_data()
            case "0": ui_exit = True