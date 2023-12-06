"""
Django settings for scm project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import datetime
from decouple import config, Csv

# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs',
        },
    },
    'loggers': {
        '__name__': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$d8&01e=mjlo33y+47z0fm^1(0rj@l&s5lyus!97mbuufp%r#%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'http://localhost:5173']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Add your React frontend's origin
    "http://127.0.0.1:5173",  # Add your React frontend's origin
]
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'https://127.0.0.1:3000',
    'https://127.0.0.1',
    'http://localhost:5173',
    'http://localhost:5174',
    # 'vercel.app',
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'inventory_management.apps.InventoryManagementConfig',
    'transaction.apps.TransactionConfig',
    'mpesa_payments.apps.MpesaPaymentsConfig',
    'custom_registration.apps.CustomRegistrationConfig',

        # 3rd party

    "rest_framework",
    # 'rest_framework_jwt',
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    'rest_auth',
    "dj_rest_auth.registration",
    'rest_framework_swagger',
    'drf_yasg',
    'corsheaders',
    'django_daraja',
    'phonenumber_field',

]

# MPESA CREDENTIALS
consumer_key=config('consumer_key')
consumer_secret=config('consumer_secret')
shortcode=config('shortcode')
pass_key=config('pass_key')
access_token_url=config('access_token_url')
checkout_url=config('checkout_url')

MPESA_ENVIRONMENT = 'sandbox'
MPESA_CONSUMER_KEY = config('consumer_key')
MPESA_CONSUMER_SECRET = config('consumer_secret')
MPESA_EXPRESS_SHORTCODE = config('shortcode')
MPESA_SHORTCODE_TYPE = 'paybill'
MPESA_PASSKEY = config('mpesa_pass_key')
MPESA_INITIATOR_USERNAME = config('initator_user_name')
MPESA_INITIATOR_SECURITY_CREDENTIAL = 'Safaricom999!*!'



SWAGGER_SETTINGS = {
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
}

SIGNALS_MODULE = 'accounts.signals'
AUTH_USER_MODEL = 'auth.User'
ROOT_URLCONF = 'scm.urls'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_EMAIL_REQUIRED = True
EMAIL_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:5173/email/confirm/"

PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:3000/password-reset/confirm/"

SITE_ID = 1
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
# Session engine and other session-related settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use the database as the session storage backend
SESSION_COOKIE_AGE = 1209600  # Set the session cookie's age (2 weeks in seconds)
ROOT_URLCONF = 'scm.urls'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

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

WSGI_APPLICATION = 'scm.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
    ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication', # new
        ],
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scm',
        'USER': 'pascal',
        'PASSWORD': 'test',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTHENTICATION_BACKENDS = (
    # ...
    'allauth.account.auth_backends.AuthenticationBackend',
    # ...
)

ACCOUNT_EMAIL_VERIFICATION = 'none'  # Disable email verification for simplicity




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Directory where uploaded media is saved.

MEDIA_URL = '/media/' # Public URL at the browser

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'