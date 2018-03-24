from api import ApiThread
from reisapi import ReisThread

# Start API
api = ApiThread(name='api')
api.start()

reis = ReisThread(name='reis')
reis.start()

api.join()
reis.join()
