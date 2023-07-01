import os
from os.path import join
from distutils.util import strtobool
import dj_database_url
from configurations import Configuration


from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):
    INSTALLED_APPS = (
        "daphne",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Third party apps
        "rest_framework",  # utilities for rest apis
        "rest_framework.authtoken",  # token authentication
        "django_filters",  # for filtering rest endpoints
        "channels",
        "channels_redis",
        # Your apps
        "backend.users",
        "posts",
        "backend",
        "companies",
        "chats",
        "drf_spectacular",
        "corsheaders",
    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
    )

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
    ]

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = "backend.urls"
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
    ASGI_APPLICATION = "backend.asgi.application"

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    ADMINS = (("Author", "rashadphilizaire@gmail.com"),)

    # Postgres
    DATABASES = {
        "default": dj_database_url.config(
            default="postgres://postgres:@localhost:5432/vision_dev",
            conn_max_age=int(os.getenv("POSTGRES_CONN_MAX_AGE", 600)),
        )
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = "UTC"
    LANGUAGE_CODE = "en-us"
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = "/"

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))
    STATICFILES_DIRS = []
    STATIC_URL = "/static/"
    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
    MEDIA_URL = "/media/"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": STATICFILES_DIRS,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.getenv("DJANGO_DEBUG", "no"))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[%(server_time)s] %(message)s",
            },
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "handlers": {
            "django.server": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["mail_admins", "console"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {"handlers": ["console"], "level": "INFO"},
        },
    }

    # Custom user app
    AUTH_USER_MODEL = "users.User"

    # Django Rest Framework
    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
        "PAGE_SIZE": 10,
        "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
        "DEFAULT_RENDERER_CLASSES": (
            "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
            "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
        ),
        "DEFAULT_PARSER_CLASSES": (
            "djangorestframework_camel_case.parser.CamelCaseFormParser",
            "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
            "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        ),
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

    SPECTACULAR_SETTINGS = {
        "SERVERS": [
            {"url": "http://127.0.0.1:8000", "description": "Local dev server"}
        ],
        "POSTPROCESSING_HOOKS": [
            "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields"
        ],
    }

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("redis", 6379)],
            },
        },
    }
