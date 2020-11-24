from settings import *
import os

PROJECT_HOME = os.path.dirname(os.path.dirname(__file__))
LOG_FOLDER=os.path.join(PROJECT_HOME, '..', 'logs')

if os.path.exists(os.path.join(PROJECT_HOME,"local_settings.py")):
    from local_settings import *
    
LOG_LEVEL="DEBUG"
LOG_FILENAME="operations_management.log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(LOG_FOLDER, LOG_FILENAME),
            'formatter': 'verbose',
            'maxBytes':604800,
            'backupCount':50
        }
    },
    'loggers': {
        'django': {
            'handlers':['mail_admins',],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.db.backends.schema': {
            'handlers':['null',],
            'propagate': True,
            'level':'INFO',
        },
        '': {
            'handlers': ['file',],
            'propagate': True,
            'level': LOG_LEVEL
        }
    },
}
