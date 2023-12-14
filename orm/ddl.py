from dml import User
import sqlalchemy

Base = sqlalchemy.orm.declarative_base()

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

def main():
    class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    location = sqlalchemy.Column('geom',Geometry(geometry_type='POINT', srid=4326))



if __name__ == __main__:
    main()