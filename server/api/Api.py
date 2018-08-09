from flask import Flask

from lib.Config import Config
from lib.Redis import Redis

api = Flask(__name__)
redis = Redis(Config['REDIS']['host'], Config['REDIS']['port'])
