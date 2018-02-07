"""
Django settings for erppapatong project on Heroku. For more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "*p39!8ej!c5^git$6lav=7%l^bua^&xk3j#!)wq@5=%@pr!yx)"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    #APP USER
    'erpp_main.apps.ErppMainConfig',
    'erpp_auth.apps.ErppAuthConfig',
    'erpp_dasboard.apps.ErppDasboardConfig',
    #APP ADMIN
    '_erpp_mainadmin.apps.ErppMainadminConfig',
    '_erpp_authadmin.apps.ErppAuthadminConfig',
    '_erpp_dasboardadmin.apps.ErppDasboardadminConfig',
    #APP REST FRAMEWORK
    'rest_framework.apps.RestFrameworkConfig',
    #APP API ADMIN
    '_erpp_apiadmin.apps.ErppApiadminConfig',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
}

#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
#SESSION_ENGINE = 'django.contrib.sessions.backends.file'
#SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

#Handle session is not Json Serializable
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_AUTO_LOGOUT = 60 #minute

#DATABASE CACHING
#CACHES = {
#   'default': {
#      'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#     'LOCATION': 'django_cache',
#}
#}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'erpp_auth.middleware.ErpAuthSessionExpiredMiddleware',
    '_erpp_authadmin.middleware.ErpAuthAdminSessionExpiredMiddleware',
]

ROOT_URLCONF = 'erppapatong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/erppapatong/templates/',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'erppapatong.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # LOCALHOST
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'erppapatong',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        # HEROKU
        #  'ENGINE': 'django.db.backends.postgresql',
        #  'NAME': 'd8e9l1plnimlfh',
        #  'USER': 'tcmrblavnntcqa',
        #  'PASSWORD': '3052fc5683caa9e2d147028aed08ee0d9a08df540fe70403f6c6ac46a66b527e',
        #  'HOST': 'ec2-107-21-95-70.compute-1.amazonaws.com',
        #  'PORT': '5432',
    }
}

# POSTGRESQL HEROKU
#Host : ec2-23-21-162-90.compute-1.amazonaws.com
#Database : devomk6sq9q21o
#User : phnfgaxaggnjij
#Port : 5432
#Password : cf4d75cb3289d27af45fe78105e69fd8c0f7d3ea94bc1ff154fd749d7b8b0832
#URI : postgres://phnfgaxaggnjij:cf4d75cb3289d27af45fe78105e69fd8c0f7d3ea94bc1ff154fd749d7b8b0832@ec2-23-21-162-90.compute-1.amazonaws.com:5432/devomk6sq9q21o
#heroku pg:psql postgresql-silhouetted-82142 --app erppapatong


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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Change 'default' database configuration with $DATABASE_URL.
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
#STATIC_URL = 'http://localhost/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


#SERVER LOCAL
SERVER_SCHEMES = 'http://'
DOMAIN_NAME = 'localhost:8000'
#SERVER HEROKU
# SERVER_SCHEMES = 'https://'
# DOMAIN_NAME = 'erppapatong.herokuapp.com'

#CHECKCONNECTIONTOINTERNET
SERVER_CHECK_CONNECTION_TO = 'www.google.com' #CHECK INTERNET CONNECTION VIA GOOGLE

#APPLICATION NAME
APP_NAME = 'ERP Papatong'
CORP_NAME = 'PT Papatong Indonesia'
CORP_ADDRESS = 'Jalan Domain Name System'

#EMAIL CONFIGURATION
APP_EMAIL = 'noreply@papatong.com' #EMAIL SENDER
BCC_EMAIL = ['trijaruto@gmail.com',]
BCC_EMAIL_ACTIVE = False
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

#EXPIRED LINK EMAIL
#FOR USER
EMAIL_ACTIVATION_EXPIRED = 30 #Minutes
EMAIL_RESET_PASSWORD_EXPIRED = 30 #Minutes
#FOR ADMIN
EMAIL_RESET_PASSWORD_ADMIN_EXPIRED = 30 #Minutes
EMAIL_REQUEST_ACTIVATION_ADMIN_EXPIRED = 4320 #Minutes
EMAIL_ACTIVATION_ADMIN_EXPIRED = 4320 #Minutes


#DEFAULT RESET USERNAME AND PASSWORD ADMINISTRATOR
APP_DEFAULT_ACCOUNT_ADMINISTRATOR_RESET = True
APP_DEFAULT_ACCOUNT_ADMINISTRATOR_USERNAME = 'trijaruto@gmail.com'
APP_DEFAULT_ACCOUNT_ADMINISTRATOR_TYPE = ['ADMINISTRATOR','ADMIN']
APP_DEFAULT_ACCOUNT_ADMINISTRATOR_RANDOM_PASSWORD_DIGIT = 6 #random digit e.x : 070183

#RECAPTCHA GOOGLE
RECAPTCHA_SITEVERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
#LOCAL
RECAPTCHA_SITEKEY = '6Ldn6w4UAAAAAEuJuTMPWi6tm-1c1N1eSX3oyvtx'
RECAPTCHA_SECRETKEY = '6Ldn6w4UAAAAAE7qISWKta73KUmvvzQUkWl7Tu_A'
#PRODUCTION
# RECAPTCHA_SITEKEY = '6LdPPUAUAAAAAK5ZHApFQEMSe-xxAeOLCkdELICa'
# RECAPTCHA_SECRETKEY = '6LdPPUAUAAAAADOww0h-h78ULLu57-3HS6vuU0SF'

#UPLOAD FILE
APP_UPLOAD_FILE_TYPE = 'cloudinary'
#APP_UPLOAD_FILE_TYPE = 'localhost'

#AES CRYPTO
AES_KEY = 'com.gnotapap.erp'
#AES_KWARGS = 'nerftrams.duolc/'
