from application import db, login_manager, app
from flask_login import UserMixin
import datetime
from sqlalchemy.sql import func


# A requirement of flask-login, let it know how to handle login_user and logout_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# A user table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Fields such as email, password, and name
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    confirm = db.Column(db.Boolean, nullable=False, default=False)

    username = db.Column(db.String, unique=True, nullable=False)

    profile_picture = db.Column(db.String, nullable=False, default='blank_profile_picture.png')

    messages = db.relationship('Message', backref='user', lazy=True)
    commands = db.relationship('Command', backref='user', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)
    message_rendered = db.Column(db.String)
    date_sent = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
            nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'),
            nullable=False)


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    trigger_phrase = db.Column(db.String, nullable=False)
    code = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
            nullable=False)

chat_to_user_association_table = db.Table('chat_to_user',
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("User", secondary=chat_to_user_association_table, backref="chats")
    room_name = db.Column(db.String, nullable=False)
    messages = db.relationship('Message', backref='chat', lazy=True)
