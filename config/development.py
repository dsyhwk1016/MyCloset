from pymongo import MongoClient

from config.default import *
from flask import Flask

# Flask App Setup
app = Flask(__name__)

# Google Setup
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
app.secret_key = os.getenv('secret_key')

# http / https 환경설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# MongoDB Setup
client = MongoClient('localhost', 27017)
db = client.mycloset

# google blueprint Setup
blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"],
)
app.register_blueprint(blueprint, url_prefix="/login")
