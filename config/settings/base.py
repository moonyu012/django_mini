import os
import random
from datetime import timedelta
from pathlib import Path


from dotenv import load_dotenv

load_dotenv('./.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent




# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@o8dbg3he9hv0-g3ja%#7spn5^_ulk*=w11n8mjw@w8(x++lys'




# 장고 기본 앱
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 추가 앱
CUSTOM_APPS =[
    'users',
    'restaurants',
    'reservations',
]

# 써드 파티 앱
THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt'
]


INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME','postgres'), # DB 이름
        'USER':os.environ.get('DB_USER','postgres'), # DB 연결할 유저
        'PASSWORD':os.environ.get('DB_PASSWORD','postgres'),# DB 접속 유저의 비밀번호
        'HOST':os.environ.get('DB_HOST','localhost'), # DB 연결 시 사용한 호스트(ip 주소, localhost=127.0.0.1)
        'PORT':os.environ.get('DB_PORT',5432), # DB 연결 시 사용할 PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'ASIA/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60), # 60분 마다 만료
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True, # 라스트 로그인 업데이트
}

KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID', random.randint)
KAKAO_REDIRECT_URI = os.environ.get('KAKAO_REDIRECT_URI', 'http://127.0.0.1:8000/api/v1/users/kakao/callback/')
KAKAO_CLIENT_SECRET = os.environ.get('KAKAO_CLIENT_SECRET')