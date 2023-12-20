import sqlalchemy
from orm.ddl import User
import os
import dotenv
from sqlalchemy.orm import sessionmaker
from orm.base import Base


env = dotenv.load_dotenv('./.env')
db_params = sqlalchemy.engine.URL.create(
    drivername='postgresql',
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"))


def create_engine()-> sqlalchemy.engine.Engine:
    """
    Creates and returns a SQLAlchemy engine using the provided database parameters.

    Returns:
        engine: A SQLAlchemy engine object.
    """
    engine = sqlalchemy.create_engine(db_params)
    return engine


def create_session(engine: sqlalchemy.engine.Engine)-> sqlalchemy.orm.Session:
    """
    Create a new session using the provided engine.

    Args:
        engine: The SQLAlchemy engine to bind the session to.

    Returns:
        A new session object.

    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_table(engine: sqlalchemy.engine.Engine)-> None : 
    """
    Create tables in the database if they don't exist or drop and create if their structure has changed.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine object.

    Returns:
        None
    """
    inspector = sqlalchemy.inspect(engine)
    if User.__tablename__ not in inspector.get_table_names():
        Base.metadata.create_all(engine)
        return
        
def create_user(session, user_nick:str, user_name:str, user_posts:int, user_city:str)->None:
    """
    Creates a new user and adds it to the session.

    Args:
        session (Session): The SQLAlchemy session object.
        user_nick (str): The nickname of the user.
        user_name (str): The name of the user.
        user_posts (int): The number of posts made by the user.
        user_city (str): The city where the user resides.

    Returns:
        User: The newly created user object.
    """
    try:
        user = User(nick=user_nick, name=user_name, posts=user_posts, city=user_city)
        session.add(user)
        session.commit()
    except:
        session.rollback()
        print("Błąd przy dodawaniu użytkownika do bazy danych. Czy struktura tabeli jest poprawna?\nSpróbuj wykonać reset bazy danych komendą 'reset' w menu.")
        
def is_unique_nick(session, user_nick:str)->bool:
    """
    Checks if the provided nickname is unique.

    Args:
        session (Session): The SQLAlchemy session object.
        user_nick (str): The nickname to check.

    Returns:
        bool: True if the nickname is unique, False otherwise.
    """
    result = session.query(User).filter(User.nick == user_nick).all()
    if len(result) == 0:
        return True
    else:
        return False
    
def user_from_nick(session, user_nick:str)->User:
    """
    Retrieves a user object from the database using the provided nickname.

    Args:
        session (Session): The SQLAlchemy session object.
        user_nick (str): The nickname of the user.

    Returns:
        User: The user object.
    """
    try:
        result = session.query(User).filter(User.nick == user_nick).first()
    except:
        print("Błąd przy pobieraniu użytkownika z bazy danych. Czy struktura tabeli jest poprawna?\nSpróbuj wykonać reset bazy danych komendą 'reset' w menu.")
        return None
    return result

def reset_table(engine: sqlalchemy.engine.Engine):
    """
    Drops the table and recreates it.

    Returns:
        None
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return