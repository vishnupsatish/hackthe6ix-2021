from application import socketio
from flask_socketio import emit, send, leave_room, join_room
from flask import session
from flask_login import current_user
from application.models.general import *
from application import db


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')

    user = User.query.filter_by(username=current_user.username).first()
    chat = Chat.query.filter_by(room_name=room).first()
    msg_db = Message(message=message['message'], message_rendered=message['message'], user=user, chat=chat)
    db.session.add(msg_db)
    db.session.commit()

    emit('message', {'msg': message['message'], 'user': current_user.username, 'pfp': current_user.profile_picture}, room=room)



@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
