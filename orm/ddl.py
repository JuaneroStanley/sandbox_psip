import sqlalchemy
from orm.base import Base


class User(Base):
    __tablename__ = "users_78712"
    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.Sequence('user_id_seq'), autoincrement=True, primary_key=True)
    nick = sqlalchemy.Column(sqlalchemy.String, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    posts = sqlalchemy.Column(sqlalchemy.Integer)


