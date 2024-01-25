from pathlib import Path
import os
import datetime
from decouple import config, Csv
from dotenv import load_dotenv
import json
from custom_registration.custom_email_backend import OAuthEmailBackend

import dj_database_url
# Load environment variables from .env
load_dotenv()

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

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_TRUSTED_ORIGINS = ['http://localhost:5173']
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
    # 'accounts.apps.AccountsConfig',
    'inventory_management.apps.InventoryManagementConfig',
    'transaction.apps.TransactionConfig',
    'slaughter_house.apps.SlaughterHouseConfig',
    'mpesa_payments.apps.MpesaPaymentsConfig',
    'custom_registration.apps.CustomRegistrationConfig',
    'invoice_generator.apps.InvoiceGeneratorConfig',
    'invoices',
    'payments',
    'logistics',

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

# EQUITY BANK CREDENTIALS
# Read Jenga credentials from .env file
JENGA_MERCHANT_CODE = config('JENGA_MERCHANT_CODE')
JENGA_CONSUMER_SECRET = config('JENGA_CONSUMER_SECRET')
JENGA_API_KEY = config('JENGA_API_KEY')
# PRIVATE_KEY_PATH = config('PRIVATE_KEY_PATH', 'privatekey.pem')
CURRENCY_CODE = config('currencyCode')

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

# SWAGGER_SETTINGS = {
#     'LOGIN_URL': 'rest_framework:login',
#     'LOGOUT_URL': 'rest_framework:logout',
# }

# SIGNALS_MODULE = 'custom_registration.signals'
# start gmail
AUTH_USER_MODEL = 'custom_registration.CustomUser'
# USERNAME_FIELD = 'email'

# PASSWORD_RESET_CONFIRM_URL = 'password_reset_confirm'

ROOT_URLCONF = 'scm.urls'
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'allauth.account.auth_backends.AuthenticationBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use the appropriate port for your SMTP server
EMAIL_USE_TLS = True  # Set to False if your server doesn't use TLS
EMAIL_HOST_USER = 'intellima.tech@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'txqerssmxheiyruz'
# EMAIL_HOST_USER = 'pascalouma54@gmail.com'  # Your email address
# EMAIL_HOST_PASSWORD = 'jcfgolmahddantnv'
# EMAIL_USE_SSL = False

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
                # 'allauth.account.context_processors.account',
                # 'allauth.socialaccount.context_processors.socialaccount',
            ],
        },
    },
]

WSGI_APPLICATION = 'scm.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    # ],
    # # ...
}

# AWS settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')

# Configure S3 for serving static files.
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Configure S3 for serving media files.
AWS_S3_PUBLIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_URL = f'{AWS_S3_PUBLIC_URL}/uploads/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Use the default storage for media files.
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Set the media URL to the S3 public URL.
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#     'rest_framework.permissions.IsAuthenticated',
#     ],
#         'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.TokenAuthentication', # new
#         ],
# }

# JWT_AUTH = {
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
# }

# AUTH_USER_MODEL = 'custom_registration.CustomUser'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'supplies',
#         'USER': 'pascal',
#         'PASSWORD': 'test',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


# DATABASES["default"] = dj_database_url.parse("postgres://scm_hxp4_user:XVYlpiSofsxlM9hYbi9uSABhgm0H8Zsg@dpg-cmodpt6d3nmc739kni6g-a.oregon-postgres.render.com/scm_hxp4")

# AUTHENTICATION_BACKENDS = (
#     # ...
#     'allauth.account.auth_backends.AuthenticationBackend',
#     # ...
# )

# AUTHENTICATION_BACKENDS = [
#     'custom_registration.backends.EmailBackend',  # Replace with the path to your custom email backend
# ]


ACCOUNT_EMAIL_VERIFICATION = 'none'  # Disable email verification for simplicity



# Password validationApp passwords
# App passwords help you sign in to your Google Account on older apps and services that don’t support modern security standards.

# App passwords are less secure than using up-to-date apps and services that use modern security standards. Before you create an app password, you should check to see if your app needs this in order to sign in.

# 

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

# MEDIA_URL = '/media/' # Public URL at the browser

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

