from .default import * # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'estoudebike',
        'USER': 'postgres',
        'TEST': {
            'NAME': 'travis_ci_test'
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
