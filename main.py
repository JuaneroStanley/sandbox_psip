# from utils.my_functions import *
import os
import dotenv

dotenv.load_dotenv('./.env')
print(os.getenv('POSTGRES_PORT'))

# load_data()
# ui()
