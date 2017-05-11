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


