from pathlib import Path
import os


# GENERAL : ================================================================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-r0rhv6&#54c6(s72&oc^4y6@wysrj%xzv997tqyw_%a!dudf=s'

DEBUG = True

INSTALLED_APPS = [
    'airline_reservation_system',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External Packages
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Airline.urls'

WSGI_APPLICATION = 'Airline.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

# USE_TZ = True

USE_TZ = False

# NETWORK : ===============================================================================================================

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True   

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     'http://127.0.0.1:3000',
#     'http://127.0.0.1:8000',
#     'http://sky-seat-saver.azurewebsites.net',
#     'http://project-mysql.mysql.database.azure.com'
# ]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
  'accept',
  'accept-encoding',
  'authorization',
  'content-type',
  'origin',
  'dnt',
  'user-agent',
  'x-csrftoken',
  'x-requested-with']

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = 'None'

CSRF_COOKIE_SAMESITE = 'None'


# DATABASE : ===============================================================================================================

DATABASES = {
    'default': { #mysql private
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'ars',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',   # Or an IP Address that your DB is hosted on
        'PORT': '3308',
    }
    # 'default': { #mysql azure
    #     'ENGINE': 'django.db.backends.mysql', 
    #     'NAME': 'ars',
    #     'USER': 'Cat',
    #     'PASSWORD': 'Murka1234',
    #     'HOST': 'project-mysql.mysql.database.azure.com',   # Or an IP Address that your DB is hosted on
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         'ssl': {'ca': './DigiCertGlobalRootCA.crt.pem'},
    #     }
    # }
}


# MODELS : ============================================================================================

AUTH_USER_MODEL = "airline_reservation_system.Users" 

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGORESIZED_DEFAULT_SCALE = 0.5
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = False
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}


# STATIC : =================================================================================================================

os.path.join(BASE_DIR, "/web-design/staticfiles-django/")
STATIC_URL = "/web-design/staticfiles-django/"
STATIC_ROOT = BASE_DIR + "/web-design/staticfiles-django/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# TEMPLATES :  =============================================================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'ars-web/build/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# LOGS : =================================================================================================================

FORMATTERS = (
    {
        "verbose": { 
            "format": "<| {levelname} - {asctime:s} - {name} - {threadName} - {thread:d} - {module} - {filename} - {lineno:d} - {name} - {funcName} - {process:d} - {message} |>",
            "style": "{",
        },
        "simple": {
            "format": "<| {levelname} - {asctime:s} - {name} - {module} - {filename} - {funcName} - {lineno:d} - {message} |>",
            "style": "{",
        },
        "short": {
            "format": "<| {levelname} - {asctime:s} - {name} - {filename} - {funcName} - {message} |>",
            "style": "{",
        },
    },
)

HANDLERS = {
    "console_handler": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
        "level": "DEBUG"
    },
    "info_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{BASE_DIR}/Airline/logs/airline_info.log",
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "short",
        "level": "INFO",
        "backupCount": 2,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    "error_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{BASE_DIR}/Airline/logs/airline_error.log",
        "mode": "a",
        "formatter": "verbose",
        "level": "WARNING",
        "backupCount": 2,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    "will_handle": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{BASE_DIR}/Airline/logs/airline_liner.log",
        "mode": "a",
        "formatter": "simple",
        "level": "DEBUG",
        "backupCount": 2,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
}

LOGGERS = (
    {   
        "django": {
            "handlers": ["console_handler", "info_handler"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["error_handler"],
            "level": "INFO",
            "propagate": True,
        },
        "django.template": {
            "handlers": ["error_handler"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.server": {
            "handlers": ["error_handler"],
            "level": "INFO",
            "propagate": True,
        },
        "pick.me": { # I will be using only this one, but will keep the other ones here too for the convenience of future me.
            "handlers": ["will_handle"],
            "level": "INFO",
            "propagate": True,
        },
    },
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # IDK what the next three do, but I guess that they enable the separation of the (Fs, Hs and Ls)'s settings by referring to them here shortly like that. The separation sure does makes it easier to read.
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS[0],
}

# API: =================================================================================================================

LOGIN_URL = "airline_reservation_system:login"
LOGIN_REDIRECT_URL = "airline_reservation_system:index"
LOGOUT_REDIRECT_URL = "airline_reservation_system:login"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    )
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Airline Reservation System',
    'COMPONENT_SPLIT_REQUEST': True,
}