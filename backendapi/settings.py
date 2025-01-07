from pathlib import Path
from datetime import timedelta
import os
import warnings


warnings.filterwarnings("ignore", category=UserWarning, module="environ")
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

SECRET_KEY = 'django-insecure-3dy!tq&dteytu=zfj2)k%*u0dt9ws&1(j8nsu!^3-3th5^*f^='

DEBUG = True

#<<<<<<< HEAD
<<<<<<< HEAD
#ALLOWED_HOSTS = ['127.0.0.1','holanine.icu']
# ALLOWED_HOSTS = ['192.168.1.8']

#CSRF_TRUSTED_ORIGINS = ['https://*.holanine.icu','https://*.127.0.0.1']
#=======
ALLOWED_HOSTS = ['139.59.9.70','demoadmin.hola9.com']
=======
ALLOWED_HOSTS = ['127.0.0.1','holanine.icu']
# ALLOWED_HOSTS = ['192.168.1.8']

CSRF_TRUSTED_ORIGINS = ['https://*.holanine.icu','https://*.127.0.0.1']
#=======
ALLOWED_HOSTS = ['127.0.0.1','139.59.9.70','demoadmin.hola9.com']
>>>>>>> 8a72e49cd22e840587db7c1423cb1ca18330101d
# ALLOWED_HOSTS = ['192.168.1.8']

#CSRF_TRUSTED_ORIGINS = ['https://*.holanine.icu','https://*.127.0.0.1']

CSRF_TRUSTED_ORIGINS = [
	'https://demoadmin.hola9.com',
	'http://139.59.9.70:8000',
]

#>>>>>>> 926376c (server side commite)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_simplejwt',
    'account',
    'pagesapi',
    'adsapi',
    'blogsapi',
    'profileapi',
    'otp_reg',
    'commentbox',
    'blogscommentbox',
    'paymentapi',
    'analysis', 
    'openMoney',
    # 'payu'
    'django_cron',
<<<<<<< HEAD
=======
    
>>>>>>> 8a72e49cd22e840587db7c1423cb1ca18330101d
    'hobby',
    'food',
    'health',
    'book_media',
    'science_technology',
    'childrens_books',
    'gadgets',
#<<<<<<< HEAD
    'farmingandgardening',
    'Vehicles_and_Spares_Parts',
    'ToysandGames',
    'photographyequipments',
    'healthandbeauty',
    'fashion',
#=======
#>>>>>>> 926376c (server side commite)
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
    # 'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'backendapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,], # add TEMPLATES_DIR that we defined above
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

WSGI_APPLICATION = 'backendapi.wsgi.application'

CORS_ALLOW_ALL_ORIGINS: True
CORS_ORIGIN_WHITELIST = ['http://localhost:8000', 'http://example.com']


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'holatwo',      
#         'USER': 'root',       
#         'PASSWORD': 'Mukesh@7260', 
#         'HOST': 'localhost',                
#         'PORT': '3306',                     
#     }
# }
CORS_ALLOW_ALL_ORIGINS = True

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL ='account.User'

MEDIA_ROOT = os.path.join(BASE_DIR,'adsapi/media')

MEDIA_URL = '/adsapi/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_RENDERER_CLASSES':('rest_framework.renderers.JSONRenderer',)
}
#SIMPLE JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=525600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer','JWT'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


PAYU_MERCHANT_KEY = "jiSsfbIQ"
PAYU_MERCHANT_SALT = "2Jt2sIH1KR"
# Change the PAYU_MODE to 'LIVE' for production.
PAYU_MODE = "TEST"

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
PASSWORD_RESET_TIMEOUT = 900
# SECURE_SSL_REDIRECT = False
# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "mk2648054@gmail.com"
EMAIL_HOST_PASSWORD = "oksrgquznllrzylj"
EMAIL_USE_TLS = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

PAYU_MERCHANT_KEY = "jiSsfbIQ"
PAYU_MERCHANT_SALT = "2Jt2sIH1KR"
# Change the PAYU_MODE to 'LIVE' for production.
PAYU_MODE = "TEST"



<<<<<<< HEAD
#CRON_CLASSES = [

 #   'adsapi.cron.MyCronJob',  # Replace 'your_app_name' with your app's name

#<<<<<<< HEAD
#]
#=======
#]
=======
CRON_CLASSES = [

    'adsapi.cron.MyCronJob',  # Replace 'your_app_name' with your app's name

#<<<<<<< HEAD
]
#=======

>>>>>>> 8a72e49cd22e840587db7c1423cb1ca18330101d
#>>>>>>> 926376c (server side commite)
