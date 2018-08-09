from gevent.wsgi import WSGIServer

from api import Api
from lib.Config import Config
from lib import Logger

# noinspection PyUnresolvedReferences
from api import Errors
from api import routes


def run():
    # Init web
    host = Config['API']['host']
    port = int(Config['API']['port'])

    Logger.info('Api running on port ' + str(port) + '.')
    server = WSGIServer((host, port), Api.api, log=None)
    server.serve_forever()
