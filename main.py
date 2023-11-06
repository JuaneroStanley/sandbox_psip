from data import user_data

for user in user_data:
    print(f'Your friend {user["nick"]} shared {user["posts"]} posts')
