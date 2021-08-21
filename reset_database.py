from application import db
from application.models.general import *

db.drop_all()

db.create_all()

user = User(username='a', email='a@a.a',
            password='$2a$12$rQ8BxT.Hy8uDPcL35s41CuB7ss1CS1QJZdz/BL.9lPR9nOiWeGf72', confirm=True)  # Password is 'a' lol

db.session.add(user)

weather = Command(title='Weather', description='Get the weather in your local timezone!', trigger_phrase='weather', code='print(\'Getting weather...\')', user=user)
news = Command(title='News', description='Get the news!', trigger_phrase='news', code='print(\'Getting news...\')', user=user)


user = User(username='b', email='b@b.b',
            password='$2a$12$rQ8BxT.Hy8uDPcL35s41CuB7ss1CS1QJZdz/BL.9lPR9nOiWeGf72', confirm=True)  # Password is 'a' lol

db.session.add(user)
db.session.add(weather)
db.session.add(news)

db.session.commit()