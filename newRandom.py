import sqlalchemy
from sqlalchemy.orm import sessionmaker

db_params = sqlalchemy.engine.URL.create(
    drivername='postgresql',
    username='postgres',
    password='psip',
    database='postgres',
    host='localhost',
    port=5432)

engine = sqlalchemy.create_engine(db_params)
connection = engine.connect()
#sql_query_1 = sqlalchemy.text("INSERT INTO mytable (name) VALUES ('Bakugan')")
#sql_query_1 = sqlalchemy.text("SELECT * FROM mytable")
#sql_query_1 = sqlalchemy.text("DELETE FROM mytable WHERE name = 'Bakugan'")
#name_to_change = input("Who to change: ")
#new_name = input("What to change to: ")
#sql_query_1 = sqlalchemy.text(f"UPDATE mytable SET name = '{new_name}' WHERE name = '{name_to_change}';")

def add_new_user():
    name = input("Enter name: ")
    sql_query_1 = sqlalchemy.text(f"INSERT INTO mytable (name) VALUES ('{name}')")
    connection.execute(sql_query_1)
    connection.commit()

def delete_user():
    name = input("Enter name: ")
    sql_query_1 = sqlalchemy.text(f"DELETE FROM mytable WHERE name = '{name}'")
    connection.execute(sql_query_1)
    connection.commit()

def update_user():
    name_to_change = input("Who to change: ")
    new_name = input("What to change to: ")
    sql_query_1 = sqlalchemy.text(f"UPDATE mytable SET name = '{new_name}' WHERE name = '{name_to_change}';")
    connection.execute(sql_query_1)
    connection.commit()
    
def list_all_users():
    sql_query_1 = sqlalchemy.text("SELECT * FROM mytable ORDER BY id ASC")
    print(connection.execute(sql_query_1).fetchall())
    
list_all_users()

#connection.execute(sql_query_1)
#connection.commit()
#Session = sessionmaker(bind=engine)
#session = Session()
#sql_query_2 = sqlalchemy.text("* FROM mytable")
#print(session.query(sql_query_2).all())




# TODO: Add to actual code datebase connection and functions to add, delete, update and list users
# TODO: Add table to database with users data
# TODO: Rewrite to object oriented code
# TODO: Sprawozdanie (strona tytułowa, spis treści, opis kodu realizującego zadanie rysowania mapy uwzględniającego opis funkcji, podsumowanie, wnioski końcowe)
