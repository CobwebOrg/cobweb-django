"""
Django settings for cobweb project.

Generated by 'django-admin startproject' using Django 1.11.3.
"""

import os
from pathlib import Path

path = Path('__file__').absolute()
while not (path.name == 'cobweb-django' or path.name == 'code'):
    path = path.parent
BASE_DIR = str(path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# cf. https://gist.github.com/ndarville/3452907
SECRET_KEY = os.environ.get('SECRET_KEY')

# Guess DEBUG and TESTING, but these should be set in settings/[environment].py

DEBUG = False
CRISPY_FAIL_SILENTLY = True
TESTING = False

INTERNAL_IPS = ['72.18.0.1']
ALLOWED_HOSTS = [
    'cobwebarchive.org',
    'dev.cobwebarchive.org',
    'localhost', 'testserver', '127.0.0.1', 'web',
]


WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

# Application definition

INSTALLED_APPS = [
    # 'whitenoise.runserver_nostatic',
    'dal',
    'dal_select2',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'countries_plus',
    'crispy_forms',
    'django_tables2',
    'haystack',
    'languages_plus',
    'phonenumber_field',
    'polymorphic',
    'django_react_templatetags',
    'rest_framework',
    'reversion',
    'webpack_loader',

    'core',
    'jargon',
    'projects',
    'webarchives',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cobweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_react_templatetags.context_processors.react_context_processor',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'cobweb.wsgi.application'


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr:8983/solr/cobweb',
        'ADMIN_URL': 'http://solr:8983/solr/admin/cores',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'core.signal_processor.CobwebSignalProcessor'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
)

AUTH_USER_MODEL = 'core.User'


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

try:
    STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT'] 
except KeyError:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]

try:
    EMAIL_HOST = os.environ['COBWEB_EMAIL_HOST']
    EMAIL_PORT = os.environ['COBWEB_EMAIL_PORT']
    EMAIL_HOST_USER = os.environ['COBWEB_EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['COBWEB_EMAIL_HOST_PASSWORD']
    EMAIL_USE_TLS = os.environ['COBWEB_EMAIL_USE_TLS']
    EMAIL_USE_SSL = os.environ['COBWEB_EMAIL_USE_SSL']
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
except KeyError:
    pass


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'
