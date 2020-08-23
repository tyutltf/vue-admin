from settings.dev import *

DEBUG = False
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:print(123)@127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'DECODE_RESPONSES':'utf8',
        }
    }
}