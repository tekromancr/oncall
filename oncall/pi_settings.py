import os

IN_MEM_DB = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('/dev/shm/', 'db.sqlite3'),
    }
}
from oncall.settings import *