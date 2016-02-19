# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import fnmatch
import logging.config
import shutil

import pyinotify

from . import config as cfg
from .celery import app

logger = logging.getLogger(__name__)


class FileHandler(pyinotify.ProcessEvent):
    """An event handler for new/updated files.

    Depending on the file extension, a task is sent to a task queue for further
    asynchronous processing. Only one task per file is sent, even in case of
    multiple matches.

    """
    def process_IN_CLOSE_WRITE(self, event):
        src = event.pathname
        logger.debug('src = %s', src)
        filename = event.name.lower()
        for pattern in cfg.PATTERNS.viewkeys():
            if fnmatch.fnmatch(filename, pattern):
                try:
                    taskname = cfg.PATTERNS[pattern]
                    dst = src.replace('/data/ftp', '/isilon/sftp', 1)
                    logger.debug('dst = %s', dst)
                    shutil.move(src, dst)
                    logger.debug('task = %s', taskname)
                    app.send_task(taskname, args=[dst])
                except Exception as e:
                    logger.exception(e)
                finally:
                    break


def get_notifier():
    """Link directories being watched with an event handler.

    When a file that was opened for writing is closed, a FileHandler is
    notified.

    """
    wm = pyinotify.WatchManager()
    for watch in cfg.WATCHES:
        wm.add_watch(mask=pyinotify.IN_CLOSE_WRITE, **watch)
    notifier = pyinotify.Notifier(wm, FileHandler())
    return notifier


def main():
    notifier = get_notifier()
    notifier.loop()

if __name__ == '__main__':
    main()
