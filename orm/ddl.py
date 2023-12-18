import sqlalchemy
from base import Base


class User(Base):
    __tablename__ = "users"
    nick = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    posts = sqlalchemy.Column(sqlalchemy.Integer)


