import os

DEBUG = True
SECRET_KEY = "row the boat"
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
GOODREADS_API_KEY = 'cvLN3ZMV7bztS4vPEkwpg'
GOODREADS_SECRET =  'E9xSffpYj3jKHvALOsttTJFQ9NWc3n511B6Yv0eq9A'
