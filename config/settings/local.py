import os

from config.settings.base import *


DEBUG = True

ALLOWED_HOSTS = []

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # smtp 서버사용
EMAIL_HOST = 'smtp.naver.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True # SMTP 포트 : 587, 보안 연결(TLS) 필요 하기때문에 True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER