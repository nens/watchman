# -*- coding: utf-8 -*-

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

# https://docs.python.org/2/library/fnmatch.html
PATTERNS = {
    '*': 'proj.tasks.echo',
}

# http://seb-m.github.io/pyinotify/
WATCHES = [
    {'path': '/foo'},
    {'path': '/bar'},
]

# Files may be moved beforehand.
# This is optional.
MOVES = {
    '/foo': '/isilon/foo',
    '/bar': '/isilon/bar',
}
