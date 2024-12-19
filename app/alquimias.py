from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app import db
from app.models.models import User, Post

def validate_user_password(username, password):
    res = db.session.scalars(select(User).where(User.username == username))
    user = res.first()
    if user and user.password == password: return user
    else: return None

def user_exists(username):
    res = db.session.scalars(select(User).where(User.username == username))
    user = res.first()
    return user

def create_user(username, password, profilepic, bio, remember = False, last_login = None):
    new_user = User(
        username=username,
        password = password,
        remember = remember,
        last_login = last_login if last_login else datetime.now(),
        profilepic = profilepic,
        bio = bio
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user

def create_post(db_session: Session, body: str, user_id: int):
    new_post = Post(
        body = body,
        timestamp = datetime.now(),
        user_id = user_id

    )
    db.session.add(new_post)
    db.session.commit()

def get_timeline():
    posts = db.session.query(Post).order_by(Post.timestamp.desc()).limit(5).all()
    return posts

