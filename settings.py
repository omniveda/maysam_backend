from pathlib import Path
import os
import uuid
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Monkey patch for MySQL UUID converter issue
from django.db.backends.mysql.operations import DatabaseOperations

def convert_uuidfield_value(self, value, expression, connection):
    if value is not None:
        if isinstance(value, bytes):
            value = uuid.UUID(bytes=value)
        else:
            value = uuid.UUID(value)
    return value

DatabaseOperations.convert_uuidfield_value = convert_uuidfield_value

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-for-development')

DEBUG = True

APPEND_SLASH = False

ALLOWED_HOSTS = ['api.blackwilbur.com','145.223.22.231','blackwilbur.com', '103.180.163.123', '127.0.0.1','mercury-uat.phonepe.com', 'localhost', 'localhost:8000']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
    'backend',
    ]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
AUTH_USER_MODEL = 'backend.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://blackwilbur.com",
    "http://blackwilbur.com",
    'https://mercury-uat.phonepe.com',
    'http://127.0.0.1:5000',  # Your local frontend URL
]
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maysam',
        'USER': 'maysam_user',  # Update with your MySQL username
        'PASSWORD': 'P@ssw0rd2025!',  # Update with your MySQL password
        'HOST': '103.180.163.123',
        'PORT': '3306',
    }
}

WSGI_APPLICATION = 'backend.wsgi.application'

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

# In Django settings.py or middleware
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'  # URL prefix for static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Change 'staticfiles' to your desired directory

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Razorpay Settings
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_CcaiEoRcHpwLa5')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '56CQ6JtFime5odK2A4Vb7L1O')
RAZORPAY_CURRENCY = 'INR'

# Cloudinary Settings
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name='dmji6uxrt',
    api_key='745654639178649',
    api_secret='p3fN0OREEpKdihPeGkp6-viVbEs'
)
