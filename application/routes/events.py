from application import socketio
from flask_socketio import emit, send, leave_room, join_room
import requests
import json
from application.settings_secrets import *
from flask import session
from flask_login import current_user
from application.models.general import *
from application import db

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')

    user = User.query.filter_by(username=current_user.username).first()
    chat = Chat.query.filter_by(room_name=room).first()

    rendered = message['message']

    if '{{ weather }}' in message['message']:
        weather = json.loads(requests.get(f'http://api.weatherapi.com/v1/current.json?key={ WEATHER_API_KEY }&q=Mississauga&aqi=no').text)

        rendered = rendered.replace('{{ weather }}', f'{ weather["current"]["condition"]["text"] }, and { weather["current"]["temp_c"] }º in Mississauga')

    if '{{ basketball_score(Raptors, Warriors) }}' in message['message']:
        rendered = rendered.replace('{{ basketball_score(Raptors, Warriors) }}', '79-98')

    msg_db = Message(message=message['message'], message_rendered=rendered, user=user, chat=chat)
    db.session.add(msg_db)
    db.session.commit()

    emit('message', {'msg': rendered, 'user': current_user.username, 'pfp': current_user.profile_picture}, room=room)

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
