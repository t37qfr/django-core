import os

#Get secret settings
from secrets import sql
sql = sql.settings()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gfec^jg*cqu%a8$+p0+pa2kqg4%$0w@)ni^n%u#c%5aj9u)fz#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if os.getenv('GAE_APPLICATION', None):
    DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.appspot.com'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
    'blog2',
    'newsletter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
if os.getenv('CLOUD_SQL', None):
    DATABASES = {
        'default': {
            'ENGINE': sql['remote']['engine'],
            'NAME': sql['remote']['name'],
            'USER': sql['remote']['user'],
            'PASSWORD': sql['remote']['password'],
            'HOST': sql['remote']['host'],
            'PORT': sql['remote']['port'],
        }
    }
elif os.getenv('GAE_APPLICATION', None):
    DATABASES = {
        'default': {
            'ENGINE': sql['production']['engine'],
            'NAME': sql['production']['name'],
            'USER': sql['production']['user'],
            'PASSWORD': sql['production']['password'],
            'HOST': sql['production']['host'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

#Defualt Login URL
LOGIN_URL = '/admin/login/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
