import sqlalchemy
import geoalchemy2

class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    location = sqlalchemy.Column('geom',Geometry(geometry_type='POINT', srid=4326))