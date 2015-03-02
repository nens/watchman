# -*- coding: utf-8 -*-
"""


"""

LOGGING = {
    'version': 1,
}

# https://docs.python.org/2/library/fnmatch.html
PATTERNS = {
    '*': 'proj.tasks.echo',
}

# http://seb-m.github.io/pyinotify/
WATCHES = [
    {'path': '/tmp'},
]
