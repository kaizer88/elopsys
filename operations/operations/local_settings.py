import os
import git
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'newoperations',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ALLOWED_HOSTS = []

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#CLICKATEL SMS Settings
CLICKATEL_USERNAME = ""
CLICKATEL_PASSWORD = ""
CLICKATEL_API_ID = 000
CLICKATEL_API_URL = ""

TIME_ZONE = 'Africa/Johannesburg'




PROJECT_HOME = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT=os.path.join(PROJECT_HOME, '..')
REVISION = git.Repo(PROJECT_ROOT).head.commit.hexsha


MEDIA_ROOT = '/var/media'
STATIC_ROOT = os.path.join(PROJECT_HOME, '..','statics_collected', REVISION)