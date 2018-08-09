import redis

class Redis:
    def __init__(self, host, port):
        self._redis = redis.StrictRedis(host=host, port=port, db=0)

    def set(self, key, value):
        return self._redis.set(key, value)

    def get(self, key):
        return self._redis.get(key)

    def exists(self, key):
        return self._redis.exists(key)
