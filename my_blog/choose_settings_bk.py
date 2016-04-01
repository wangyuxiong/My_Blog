# choose settings between Developement and Deploy
import os
import platform

node = platform.node()
dev_machines = ('mac', 'metaboy-MacBook-Pro.local',)

if node in dev_machines:
    # folder My_Blog
    My_Blog = os.path.dirname(os.path.dirname(__file__))
    # project dir, contains static and media folder under DEV environment
    PROJECT_DIR = os.path.dirname(My_Blog)
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(My_Blog, 'db.sqlite3'),
        }
    }
    STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(My_Blog, 'static'),)
    MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
    MEDIA_URL = '/media/'
    TEMPLATE_DIRS = [os.path.join(My_Blog, 'templates')]
    ALLOWED_HOSTS = ['*']
else:
    DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'database1',
            'USER': 'laike9m',
            'PASSWORD': os.environ["DJANGO_DB_PASSWORD"],
            'HOST': '',
            'PORT': '',
        }
    }
    MEDIA_ROOT = '/home/laike9m/webapps/media/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = '/home/laike9m/webapps/static/'
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        '/home/laike9m/webapps/my_blog/my_blog/static/',
    )
    TEMPLATE_DIRS = (
        '/home/laike9m/webapps/my_blog/my_blog/templates',
    )
    ALLOWED_HOSTS = ['.laike9m.com', '.laike9m.webfactional.com']

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'unix:/home/laike9m/memcached.sock',
        }
    }

