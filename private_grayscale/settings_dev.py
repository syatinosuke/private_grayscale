from msilib.schema import Media
from .settings_common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s1!p2)lyq2wui47+tleza957+t4j-*jx=o8m!%x0kir9$drj5b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# ロギング設定
LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # diaryアプリケーションが利用するロガー
        'grayscale': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

# コンソール用
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Gmail用
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = "urayukki@gmail.com"
#EMAIL_HOST_PASSWORD = "wwypkmluuyecnqtg"
#DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')