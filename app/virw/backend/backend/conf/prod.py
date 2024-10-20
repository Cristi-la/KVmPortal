from .base import *
from .base import REDIS_IP, REDIS_PORT, SHARED_APPS, WEBPACK_LOADER_GET
from .base import REST_FRAMEWORK
REDIS_DEFENDER_DB = 10
REDIS_COMON_CACHE = 20

# --------------------------------------
# Security defender settings
# --------------------------------------


DEFENDER_REDIS_URL = f'redis://{REDIS_IP}:{REDIS_PORT}/{REDIS_DEFENDER_DB}'


MIDDLEWARE.append('defender.middleware.FailedLoginMiddleware')

SECRET_KEY = 'FILL_ME_IN'
ALLOWED_HOSTS = ['*']
DEBUG = False
WEBPACK_LOADER = WEBPACK_LOADER_GET(DEBUG)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f'redis://{REDIS_IP}:{REDIS_PORT}/{REDIS_COMON_CACHE}',
        'KEY_FUNCTION': 'django_tenants.cache.make_key',
        'REVERSE_KEY_FUNCTION': 'django_tenants.cache.reverse_key',
    },
}


REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
]