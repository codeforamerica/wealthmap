from primerpeso2.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sq)eck#=xcu13k0%aw)11dpqbf6hd@$e5kjel*qk2i92yckn+*'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'primerpeso2',
        'USER': 'primerpeso2',
        'HOST': 'localhost',
        'PASSWORD': 'password',
    }
}

STATIC_ROOT = '/webapps/primerpeso2/static/'
