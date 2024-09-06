from decouple import config
import os
from pathlib import Path

DEBUG = True  # Or False if you are deploying to production

ALLOWED_HOSTS = []

ROOT_URLCONF = 'crawler.urls'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'mm^w_o1_@j_ihltr1#^u8(u)g&__c5m*-)=ueh5lihbnnzk)!ogr6=3_=cdnzx&j(jdg9jpzn8z02=g667-*51brq&)2t-7t*e'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crawler',  # Your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'example',
        'HOST': 'localhost',  # Or the IP address of your database server
        'PORT': '5432',       # Default port for PostgreSQL
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'src/crawler/static'),
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


LOGOUT_REDIRECT_URL = 'logout'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

OPENAI_API_KEY = config('OPENAI_API_KEY')