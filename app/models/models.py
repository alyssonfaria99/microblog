from flask_login import UserMixin
from app import login
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    remember: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime] = mapped_column()
    profilepic: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column()
    posts: Mapped[list['Post']] = relationship(back_populates='author')

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    body: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable = False)
    author: Mapped[User] = relationship(back_populates='posts')

