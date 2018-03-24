from threading import Thread
from gevent.wsgi import WSGIServer

from api import Api
from lib.Config import Config
from lib import Logger

# noinspection PyUnresolvedReferences
from api import Errors
from api import routes


def run(port):
    Logger.info('Api running on port ' + str(port) + '.')
    server = WSGIServer(('0.0.0.0', port), Api.api, log=None)
    server.serve_forever()


class ApiThread(Thread):
    def run(self):
        run(int(Config['API']['port']))
