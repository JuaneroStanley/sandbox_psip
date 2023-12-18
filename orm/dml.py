import sqlalchemy
from ddl import User
import os
import dotenv
from sqlalchemy.orm import sessionmaker
from base import Base


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


def create_tables(engine: sqlalchemy.engine.Engine)-> None : 
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
    else:
        meta = sqlalchemy.MetaData()
        meta.reflect(bind=engine)
        table = meta.tables[User.__tablename__]
        is_same_structure = all(column.name in table.columns and isinstance(column.type, type(table.columns[column.name].type)) for column in User.__table__.columns)
        if not is_same_structure:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
        
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
    user = User(nick=user_nick, name=user_name, posts=user_posts, city=user_city)
    session.add(user)
    session.commit()
    return user

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
    
