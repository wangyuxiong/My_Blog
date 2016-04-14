# choose settings between Developement and Deploy
import os
import platform

node = platform.node()
dev_machines = ('metaboy.local',)

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
    MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
    MEDIA_URL = '/media/'
    TEMPLATE_DIRS = [os.path.join(My_Blog, 'templates')]
    ALLOWED_HOSTS = ['*']
else:
    DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'myblog_test',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '****',
            'PORT': '***',
        }
    }
    PROJECT_DIR = '/Users/metaboy/webapps/My_Blog'
    MEDIA_ROOT = '/Users/metaboy/webapps/media/'
    MEDIA_URL = '/media/'
    STATIC_ROOT = '/Users/metaboy/webapps/static/'
    STATIC_URL = '/static/'

    # PROJECT_DIR = '/home/laike9m/Envs/blog/My_Blog/'
    # MEDIA_ROOT = '/home/laike9m/media/'
    # MEDIA_URL = '/media/'
    # STATIC_ROOT = '/home/laike9m/static/'
    # STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(PROJECT_DIR, 'static'),
    )

    TEMPLATE_DIRS = (
        os.path.join(PROJECT_DIR, 'templates'),
    )

    ALLOWED_HOSTS = [
        '.wangyuxiong.com'
    ]

    # cache entire site
    MIDDLEWARE_CLASSES_ADDITION_FIRST = (
        'django.middleware.cache.UpdateCacheMiddleware',
    )

    MIDDLEWARE_CLASSES_ADDITION_LAST = (
        'django.middleware.cache.FetchFromCacheMiddleware',
    )

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
