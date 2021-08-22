from os import environ

MAIL_EMAIL = environ.get('MAIL_EMAIL')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')

SECRET_KEY = environ.get('SECRET_KEY')

CLOUDINARY_API_KEY = environ.get('CLOUDINARY_API_KEY')

CLOUDINARY_API_SECRET = environ.get('CLOUDINARY_API_SECRET')

WEATHER_API_KEY = environ.get('WEATHER_API_KEY')