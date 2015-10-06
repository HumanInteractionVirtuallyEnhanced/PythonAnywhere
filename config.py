import os
basedir = os.path.abspath(os.path.dirname(__file__))

#CSRF_ENABLED = False
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'groopieco@gmail.com'#os.environ.get('groopieco@gmail.com')
MAIL_PASSWORD = '12RedFoxes'#os.environ.get('12RedFoxes')

ADMINS = ['groopieco@gmail.com', 'rijul.gupta@yale.edu']


#
# SOCIAL_FACEBOOK = [
#     {'consumer_key': '613995812038257'},
#     {'consumer_secret': '05e778848e1187897b834fba967cc0c9'}
# ]


#
#
# from paypal import PayPalConfig
# from paypal import PayPalInterface
#
# config = PayPalConfig(API_USERNAME = "XXXXXX_XXXXXXXXXX_XXX_api1.XXXXX.XX",
#                       API_PASSWORD = "xxxxxxxxxx",
#                       API_SIGNATURE = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#                       DEBUG_LEVEL=0)
#
# interface = PayPalInterface(config=config)