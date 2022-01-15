from pathlib import Path
import os
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "server"

env = environ.Env()
path_to_env_file = os.path.join(BASE_DIR, '.env')
env.read_env(path_to_env_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5)7il2nb+8b$f2xpvnd4%r%z+^3gsh!yu5*k-)jc9ip(ppp1a5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
# DEBUG = os.environ['DEBUG']


ALLOWED_HOSTS = [
                    'localhost',
                    '127.0.0.1',
                    '[::1]',
                ] + env.list('ALLOWED_HOSTS', default=[])

# Application definition
INSTALLED_APPS = [
    # Основные приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Зависимости
    'rest_framework',
    "corsheaders",

    # Наши приложения
    'api_img.apps.ApiImgConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': env.db_url()
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': os.environ['DB_NAME'],
    #     'USER': os.environ['DB_USER'],
    #     'PASSWORD': os.environ['DB_PASSWORD'],
    #     'HOST': os.environ['DB_HOST'],
    #     'PORT': os.environ['DB_PORT'],
    # }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1'
    # 'http://localhost:8000',
    # 'http://127.0.0.1:8000'
]

CORS_ALLOW_ALL_ORIGINS=True

# Пути для сохранения загруженных изображений
# MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_ROOT = str(BASE_DIR / "media")
MEDIA_URL = "/media/"










# ------------------------------------------------------------------------------
# НАСТРОЙКИ ДЛЯ DRF
# ------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    # Классы дял пагинации
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,

    # По дефолту делаем отображение страницы API в формате JSON
    # Отключает визуальное тображение API, в место этого в браузере
    # будет отдавать чистый JSON
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    # Устанавливает правило, принимать в API только JSON
    # больше неьзя будет отправлять form-data только JSON
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # )
}











# ------------------------------------------------------------------------------
# НАСТРОЙКИ ДЛЯ CELERY
# ------------------------------------------------------------------------------
# Для работы в основной системы указываем 127.0.0.1
# Для работы внутри Docker контейнера указываем
# либо redis либо IP основной машины
# redis://<IP>:6379
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_BROKER_URL = 'redis://redis:6379'

# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 30 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
# CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"









# ------------------------------------------------------------------------------
# НАСТРОЙКИ ДЛЯ РАБОТЫ С ИЗОБРАЖЕНИЯМИ
# ------------------------------------------------------------------------------
# Директория для временного хранения настроек
DIR_TRANSFER = os.path.join(str(MEDIA_ROOT), 'images', 'api_img', 'transfer')

# Директории для загрузки больших и маленьких изображений
BIG_IMG_PATH = os.path.join('images', 'api_img', 'big')
SMALL_IMG_PATH = os.path.join('images', 'api_img', 'min')

# Ограничение в 2 MB указанное в байтах
FILE_MAX_SIZE = env.int('FILE_MAX_SIZE')

# Форматы изображений разрешенных к загрузке
UPLOAD_IMAGE = ['jpg', 'jpeg']

# Формат изображения в который будет конвертироваться результирующее изображение
CONVERT_IMG_TO_FORMAT = '.jpg'

# Использовать для стилизации нейронную сеть или заглушку
USE_NEURAL_STYLIZE = True

# Количество шагов обработки изображения нейронной сетью. По дефолту в самой функции шагов 100
QUALITY = env.int('QUALITY')

# Уровень прозрачности для генерируемых изображений
ALPHA_VALUE = 128
