from .default import * # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'estoudebike',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'TEST': {
            'NAME': 'edbtestdb'
        }
    }
}


