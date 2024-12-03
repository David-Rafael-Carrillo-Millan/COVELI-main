from decouple import config

class Config:
    SECRET_KEY = 'B!1weNAt1T%kyhUI+*S&'

class DevelopmentConfig (Config):
    DEBUG = True
    MYSQL_HOST = 'coveli-database.chyu2sssqvoz.us-east-1.rds.amazonaws.com'
    MYSQL_USER = 'usuario_remoto'
    MYSQL_PASSWORD = '20213tn051'
    MYSQL_DB = 'tienda'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 # TLS: TRANSPORT LAYER SECURITY: SEGURIDAD DE LA CAPA DE TRANSPORTE
    MAIL_USE_TLS = True
    MAIL_USERNAME = '20213tn099@utez.edu.mx'
    MAIL_PASSWORD = config('MAIL_PASSWORD')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}