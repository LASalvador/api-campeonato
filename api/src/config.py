class Config(object):
    DEBUG = True
    CSRF_ENABLED = True
    SECRET = 'olamundo'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:olamundo@mysql-container:3306/api'
    SQLALCHEMY_TRACK_MODIFICATIONS = False