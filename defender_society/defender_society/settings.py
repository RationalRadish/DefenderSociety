"""
Django settings for defender_society project.

Generated by 'django-admin startproject' using Django 2.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add apps directory
sys.path.insert(0, os.path.join(BASE_DIR,'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  os.getenv('defender_society_SECRET_KEY','7)88%-kng%o!m042sk1g9mcdt^bi9=w*(4y2)scscxe!nuu2w&')

API_FLAG = os.getenv('defender_society_API_FLAG','False').upper() =='TRUE'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('defender_society_DEBUG','True').upper() =='TRUE'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # Add humanized filter
    'django.contrib.sitemaps', # Sitemap

    'oauth', # Custom user application
    # allauth applications that need to be registered
    'django.contrib.sites', # This is built-in, it will create a sites table to store the domain name
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'rest_framework',

    'crispy_forms', # bootstrap form style
    'imagekit', # Upload image application

    'haystack', # Full text search application This should be placed before other applications
    'blog', # Blog application
   # 'tool', # tool
    #'comment', # Comment

]


# Custom user model
AUTH_USER_MODEL ='oauth.Ouser'

# allauth configuration
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# allauth required configuration
# When an error like "SocialApp matching query does not exist" appears, you need to change this ID
SITE_ID = 2

# Set the page to be redirected after successful login and registration. The default is /accounts/profile/
LOGIN_REDIRECT_URL = "/"

# Email setting
# Email verification method during registration: one of "mandatory", "optional (default)" or "none".
# If email verification is enabled, an error will be reported if the email configuration is unavailable, so it is closed by default and turned on as needed
ACCOUNT_EMAIL_VERIFICATION = os.getenv('defender_society_ACCOUNT_EMAIL_VERIFICATION','none')
# Login method, select user name or email to log in
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# Set the email address when registering the user
ACCOUNT_EMAIL_REQUIRED = True
# Logout directly exit without confirmation
ACCOUNT_LOGOUT_ON_GET = True

# Configuration of form plugin
CRISPY_TEMPLATE_PACK ='bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'defender_society.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join( BASE_DIR , 'templates' )], # set View
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.settings_info' ,   # Custom context manager
            ],
        },
    },
]

WSGI_APPLICATION = 'defender_society.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/static'
STATIC_ROOT = '/vol/web/static'

# Media file collection
MEDIA_URL ='/static/media/'
MEDIA_ROOT = '/vol/web/media'

# Unified paging settings
BASE_PAGE_BY = 10
BASE_ORPHANS = 5

# Full text search application configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE':'blog.whoosh_cn_backend.WhooshEngine', # Choose the language parser to replace the stuttering word segmentation for yourself
        'PATH': os.path.join(BASE_DIR,'whoosh_index'), # Save the address of the index file, select the home directory, this will be automatically generated
    }
}
HAYSTACK_SIGNAL_PROCESSOR ='haystack.signals.RealtimeSignalProcessor'


# restframework settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

 #Configure the database
MYSQL_HOST = os.getenv('defender_society_MYSQL_HOST', '127.0.0.1')
MYSQL_NAME = os.getenv('defender_society_MYSQL_NAME','test')
MYSQL_USER = os.getenv('defender_society_MYSQL_USER','root')
MYSQL_PASSWORD = os.getenv('defender_society_MYSQL_PASSWORD','Whiskeyman42!')
MYSQL_PORT = os.getenv('defender_society_MYSQL_PORT', 3306)

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql', # Modify the database to MySQL and configure
        'NAME': MYSQL_NAME, # The name of the database
        'USER': MYSQL_USER, # database user name
        'PASSWORD': MYSQL_PASSWORD, # database password
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'OPTIONS': {'charset':'utf8'}
    }
}

# Use django-redis to cache pages, the cache configuration is as follows:
REDIS_HOST = os.getenv('defender_society_REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('defender_society_REDIS_PORT', 6379)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}".format(REDIS_HOST, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Configure the management mailbox. If the service fails, you will receive an email. The format of the environment variable value: name|test@test.com Multiple groups of users are separated by English commas
ADMINS = []
admin_email_user = os.getenv('defender_society_ADMIN_EMAIL_USER')
if admin_email_user:
    for each in admin_email_user.split(','):
        a_user, a_email = each.split('|')
        ADMINS.append((a_user, a_email))

# Mailbox configuration
EMAIL_HOST = os.getenv('defender_society_EMAIL_HOST','smtp.163.com')
EMAIL_HOST_USER = os.getenv('defender_society_EMAIL_HOST_USER','your-email-address')
EMAIL_HOST_PASSWORD = os.getenv('defender_society_EMAIL_HOST_PASSWORD','your-email-password') # This is not an email password, but an authorization code
EMAIL_PORT = os.getenv('defender_society_EMAIL_PORT', 22)
EMAIL_TIMEOUT = 5
# Whether SSL or TLS is used, in order to use port 465, use this
#EMAIL_USE_SSL = os.getenv('IZONE_EMAIL_USE_SSL','True').upper() =='TRUE'
# The default sender, if you don’t set it, Django uses webmaster@localhost by default, so you should set it to your available mailbox
DEFAULT_FROM_EMAIL = os.getenv('defender_society_DEFAULT_FROM_EMAIL','The Defender Society <your-email-address>')

# Website default settings and contextual information
SITE_LOGO_NAME = os.getenv('defender_society_LOGO_NAME',"The Defender Society")
SITE_DESCRIPTION = os.getenv('defender_society_SITE_DESCRIPTION','Alumni Association blog for Big Brothers Big Sisters of Kentuckiana')
SITE_KEYWORDS = os.getenv('defender_society_SITE_KEYWORDS','BBSKY')
SITE_END_TITLE = os.getenv('defender_society_SITE_END_TITLE','')


# Webmaster Push
MY_SITE_VERIFICATION = os.getenv('defender_society_SITE_VERIFICATION','')

# Use http or https (the link in the sitemap can be reflected)
PROTOCOL_HTTPS = os.getenv('defender_society_PROTOCOL_HTTPS','HTTP').lower()

#'url': os.getenv('IZONE_HAO_URL','https://hao.tendcode.com')


