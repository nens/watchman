# -*- coding: utf-8 -*-

from collections import OrderedDict
import os

SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(
                BUILDOUT_DIR, 'var', 'log', 'watchman.log'),
            'formatter': 'verbose',
            'level': 'INFO',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'watchman.notify': {
            'propagate': True,
        },
    },
}

ProFTPD = True

BROKERS = {
    '3di': 'redis://redis:6379/0',
    'lizard': 'amqp://guest:guest@rabbitmq:5672//',
}

WATCHES = [
    {'path': '/srv/ftp', 'rec': True, 'auto_add': True},
]

PATTERNS = OrderedDict([
    ('/srv/ftp/priority-user/*.csv', {'broker': 'lizard', 'task': 'lizard_task', 'kwargs': {'priority': 5}}),
    ('/srv/ftp/expiring-import/*.csv', {'broker': 'lizard', 'task': 'lizard_task', 'kwargs': {'expires': 300}}),
    ('/srv/ftp/*.csv', {'broker': 'lizard', 'task': 'lizard_task'}),
    ('/srv/ftp/*.nc', {'broker': '3di', 'task': '3di_task'}),
])

MOVES = {
    '/foo': '/isilon/foo',
    '/bar': '/isilon/bar',
}
