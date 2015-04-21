from time import time
import falcon
from app.utils.rate_limit import redis_connection


class RateLimiter(object):

    def __init__(self, limit=100, window=60):
        self.limit = limit
        self.window = window
        self.redis = redis_connection()

    def process_request(self, req, res):
        requester = req.env['REMOTE_ADDR']
        if req.context['auth_user']:
            requester = req.context['auth_user']['email']
        key = "{0}: {1}".format(requester, req.path)

        try:
            remaining = self.limit - int(self.redis.get(key))
        except (ValueError, TypeError):
            remaining = self.limit
            self.redis.set(key, 0)

        expires_in = self.redis.ttl(key)
        if expires_in == -1:
            self.redis.expire(key, self.window)
            expires_in = self.window

        res.append_header('X-RateLimit-Remaining', remaining)
        res.append_header('X-RateLimit-Limit', self.limit)
        res.append_header('X-RateLimit-Reset', time() + expires_in)

        if remaining > 0:
            self.redis.incr(key, 1)
        else:
            raise falcon.HTTPError(status=429, title='Too Many Requests')
