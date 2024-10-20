from pathlib import Path
from datetime import timedelta
from kombu import Queue, Exchange
import os
# --------------------------------------
# Utils
# --------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
REDIS_IP = os.getenv("REDIS_IP", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", 0)
REDIS_CONSUMER_DB = os.getenv("REDIS_CONSUMER_DB", 1)
REDIS_CONTROLER_DB = os.getenv("REDIS_CONTROLER_DB", 2)
DEBUG = os.getenv("DEBUG", False)
# --------------------------------------
# tenant settings
# --------------------------------------
TENANT_TYPES = {
    'public': {
        "APPS": [
            'django_tenants',
            'apps.common', #  tenant model resides in this App

            'daphne',
            'channels',

            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.staticfiles',
            'django.contrib.sessions',
            'django.contrib.messages',
            "tenant_users.permissions",
            "tenant_users.tenants",

            'webpack_loader',
            'django_filters',
            'rest_framework',
            'drf_spectacular',

            'django_celery_results',
            "django_celery_beat",
            # "django_tenants_celery_beat",
            
            'rest_framework_simplejwt.token_blacklist',
            # 'defender',
        ],
        'URLCONF': 'backend.urls',
    },
    'private': {
        "APPS": [
            'django.contrib.admin',
            "django.contrib.auth",
            "django.contrib.contenttypes",
            'django.contrib.staticfiles',
            'django.contrib.sessions',
            'django.contrib.messages',
            "tenant_users.permissions",

            'django_celery_results',
            "django_celery_beat",

            'apps.private',
            'apps.kvm',
        ],
        'URLCONF': 'apps.private.urls',
    },
}

TENANT_MODEL = "common.Client"
TENANT_DOMAIN_MODEL = "common.ClientDomain"
HAS_MULTI_TYPE_TENANTS = True
MULTI_TYPE_DATABASE_FIELD = 'type'
TENANT_MULTIPROCESSING_MAX_PROCESSES = 2
TENANT_MULTIPROCESSING_CHUNKS = 2
TENANT_USERS_DOMAIN ='localhost'
AUTHENTICATION_BACKENDS = ("tenant_users.permissions.backend.UserBackend",)
# PERIODIC_TASK_TENANT_LINK_MODEL = "private.PeriodicTaskTenantLink"
# --------------------------------------
# apps settings
# --------------------------------------
AUTH_USER_MODEL = "common.TenantUser"

INSTALLED_APPS = []
for schema in TENANT_TYPES:
    INSTALLED_APPS += [app for app in TENANT_TYPES[schema]["APPS"] if app not in INSTALLED_APPS]

# --------------------------------------
# Defender settings
# --------------------------------------
DEFENDER_LOGIN_FAILURE_LIMIT = 30
DEFENDER_COOLOFF_TIME = 300
DEFENDER_LOCKOUT_TEMPLATE = "lockout.html"
SECRET_KEY = os.getenv("SECRET_KEY", "'django-insecure-wmt@)!=uf-u%=ppcu4v@2oe3kz_%=pf+id_=41-dw3!^qn+y#i'")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", '*').split(",")
# --------------------------------------
# Middleware settings
# --------------------------------------
MIDDLEWARE = [
    'backend.middleware.TenantMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "tenant_users.tenants.middleware.TenantAccessMiddleware"
    ,
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------------------------
# REST settings
# --------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "apps.common.pagination.StandardResultsSetPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_AUTHENTICATION_CLASSES": [
        'apps.private.authentication.TenantJWTAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated",],
}
SPECTACULAR_SETTINGS = {
    "TITLE": "WKVM API",
    "DESCRIPTION": "Web KVM API",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "apps.private.authentication.account_authentication_rule",

    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# --------------------------------------
# Core settings
# --------------------------------------
ASGI_APPLICATION = 'backend.asgi.application'
WSGI_APPLICATION = 'backend.wsgi.application'

# URLS/Paths -----------------------
ROOT_URLCONF = 'backend.urls'
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = 'media/'
STATICFILES_DIRS = [
    BASE_DIR / "../frontend/assets",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# ----------------------------

<<<<<<< HEAD:app/virw/backend/backend/conf/base.py
=======

ASGI_APPLICATION = 'backend.asgi.application'
# LOCAL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# PRODUCTION
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres', 
#         'USER': 'postgres',
#         'PASSWORD': 'asdf',
#         'HOST': '127.0.0.1', 
#         'PORT': '5432',
#     }
# }


>>>>>>> 5547abb4a7464bf1c092df7da4bda8dcd98808dc:WKVM/backend/backend/settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_TZ = True

<<<<<<< HEAD:app/virw/backend/backend/conf/base.py
# --------------------------------------
# Files handlers settings
# --------------------------------------    
WEBPACK_LOADER_GET = lambda DEBUG: {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "STATS_FILE": BASE_DIR / "../frontend/webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}
WEBPACK_LOADER = WEBPACK_LOADER_GET(True)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
=======
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = 'media/'

STATICFILES_DIRS = [
    BASE_DIR / "../frontend/static"
]
>>>>>>> 5547abb4a7464bf1c092df7da4bda8dcd98808dc:WKVM/backend/backend/settings.py

# --------------------------------------
# Databases settings
# --------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv("POSTGRES_DB", "virw"),
        'USER': os.getenv("POSTGRES_USER", "posgress"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", "asdf"), 
        'HOST': os.getenv("POSTGRES_HOST", "localhost"),
        'PORT': os.getenv("POSTGRES_PORT", "5432"),
    }
}
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts":[{
                "address": f'redis://{REDIS_IP}:{REDIS_PORT}',
                "db": REDIS_CONSUMER_DB,
            }]
        }
    }
}

# --------------------------------------
# Celery settings
# --------------------------------------
REDIS_URL = f'redis://{REDIS_IP}:{REDIS_PORT}/{REDIS_CELERY_DB}'
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = REDIS_URL

# Queues
CELERY_TASK_QUEUES = (
    Queue('critical', Exchange('critical'), routing_key='critical'),
    Queue('medium', Exchange('medium'), routing_key='medium'),
    Queue('low', Exchange('low'), routing_key='low'),
)
CELERY_TASK_DEFAULT_QUEUE = 'medium'

# Task settings
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TENANT_CACHE_SECONDS = 30
CELERY_BEAT_TZ_AWARE = True