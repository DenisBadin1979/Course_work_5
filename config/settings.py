import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True if os.getenv("DEBUG") == "True" else False

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "users.User"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "habits",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_celery_beat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("NAME"),
        "USER": os.getenv("USER"),
        "PASSWORD": os.getenv("PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT", default="5432"),
    }
}

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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

# Настройки JWT-токенов
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# Настройки срока действия токенов
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


CELERY_BEAT_SCHEDULE = {
    "task-every-1-days": {
        "task": "habits.tasks.some_task_1d",
        "schedule": crontab(hour=0, minute=0),
    },
    "task-every-2-days": {
        "task": "habits.tasks.some_task_2d",
        "schedule": timedelta(days=2),
    },
    "task-every-3-days": {
        "task": "habits.tasks.some_task_3d",
        "schedule": timedelta(days=3),
    },
    "task-every-4-days": {
        "task": "habits.tasks.some_task_4d",
        "schedule": timedelta(days=4),
    },
    "task-every-5-days": {
        "task": "habits.tasks.some_task_5d",
        "schedule": timedelta(days=5),
    },
    "task-every-6-days": {
        "task": "habits.tasks.some_task_6d",
        "schedule": timedelta(days=6),
    },
    "task-every-7-days": {
        "task": "habits.tasks.some_task_7d",
        "schedule": timedelta(days=7),
    },
}
CELERY_BROKER_URL = "redis://redis:6379/0"  # Например, Redis, который по умолчанию работает на порту 6379

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

# Часовой пояс для работы Celery
CELERY_TIMEZONE = TIME_ZONE

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

TELEGRAM_URL = "https://api.telegram.org/bot"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
