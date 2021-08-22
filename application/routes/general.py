from types import SimpleNamespace
from flask import render_template, flash, redirect, url_for, jsonify, request, abort, session
from application import app, db
import secrets
import slugify
from .account import abort_not_confirmed
import cloudinary
import cloudinary.uploader
import cloudinary.api
from application.settings_secrets import *
from flask_login import login_required, current_user
from application.models.general import *

@app.template_filter()
def filter_list(l, command):
    return list(filter(eval(command), l))

@app.route('/')
@app.route('/dashboard')
@login_required
@abort_not_confirmed
def dashboard():
    # Your home logic goes here
    context = {}
    context['userid'] = current_user.username
    context['email'] = current_user.email
    
    return render_template('general/dashboard.html', context=context, page_title='Dashboard')

@app.route('/chat')
@login_required
@abort_not_confirmed
def chat():
    return render_template('general/chat.html', chats=current_user.chats, active=None, page_title='Chat')

@app.route('/add-chat', methods=['POST'])
@login_required
@abort_not_confirmed
def add_chat():
    try:
        username = request.form['username']
    except KeyError:
        abort('Input data is of an invalid form.', 400)
        
    chat_with = User.query.filter_by(username=username).first()

    chat = Chat()
    chat.users.append(chat_with)
    chat.users.append(current_user)

    chat.room_name = f'{current_user.username}-{chat_with.username}'

    db.session.add(chat_with)
    db.session.add(chat)
    db.session.commit()
    
    return redirect('chat')

@app.route('/chat/<string:room>')
@login_required
@abort_not_confirmed
def chat_person(room):
    print(room)
    chat = Chat.query.filter_by(room_name=room).first_or_404()

    if not current_user in chat.users:
        abort(404)

    session['room'] = room

    return render_template('general/specific-chat.html', chats=current_user.chats, active=chat.room_name, chat=chat, page_title='Chat')


@app.route('/commands', defaults={'command': None}, methods=['GET', 'POST', 'PATCH'])
@app.route('/commands/<string:command>')
@login_required
@abort_not_confirmed
def commands(command):
    if request.method == "GET":
        commands = Command.query.all()
        command = Command.query.filter_by(title=command).first()
        
        return render_template('general/commands.html', commands=commands, active=command, page_title='Command')
    elif request.method == "PATCH":
        try:
            _id = request.form['id']
            description = request.form['description']
            trigger_phrase = request.form['trigger_phrase']
            code = request.form['code']
        except KeyError:
            return abort('Input data is of an invalid form.', 400)

        new_command = Command.query.get(_id)
        new_command.description = description
        new_command.code = code
        new_command.trigger_phrase = trigger_phrase
        db.session.commit()
        
        return 'Hello'
    else:
        try:
            title = request.form['title']
            description = request.form['description']
            trigger_phrase = request.form['trigger_phrase']
            code = request.form['code']
        except KeyError:
            return abort('Input data is of an invalid form.', 400)

        new_command = Command(title=title, description=description, trigger_phrase=trigger_phrase, code=code, user_id=current_user.id)
        db.session.add(new_command)
        db.session.commit()

        return 'Hello'

@app.route('/upload', methods=['POST', 'GET'])
@login_required
@abort_not_confirmed
def upload():
    cloudinary.config(cloud_name = 'hackthe6ixproject', api_key=CLOUDINARY_API_KEY, api_secret=CLOUDINARY_API_SECRET)
    upload_result = None
    if request.method == 'POST':
        try:
            file_to_upload = request.files['file']
        except KeyError:
            return abort(400, 'Cannot find file in request.')
        if file_to_upload:
            token = secrets.token_hex(16)
            upload_result = cloudinary.uploader.upload(file_to_upload, public_id=f'{token}')
            current_user.profile_picture = f'{token}.{file_to_upload.filename.split(".")[-1]}'
            db.session.commit()
            # app.logger.info(upload_result)
            return redirect(url_for('dashboard'))
    return abort(400, 'Cannot find file in request.')

