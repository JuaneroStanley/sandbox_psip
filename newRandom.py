import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
a = load_dotenv()


db_params = sqlalchemy.engine.URL.create(
    drivername='postgresql',
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"))

engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
sql_query_1 = sqlalchemy.text("SELECT name FROM mytable WHERE name = 'Kowalczyk'")
result = connection.execute(sql_query_1)
result = [r for r in result]
for character in result:
    var = (character[0])
print (var)


# TODO: Add to actual code datebase connection and functions to add, delete, update and list users
# TODO: Add table to database with users data
# TODO: Rewrite to object oriented code
# TODO: Sprawozdanie (strona tytułowa, spis treści, opis kodu realizującego zadanie rysowania mapy uwzględniającego opis funkcji, podsumowanie, wnioski końcowe)
