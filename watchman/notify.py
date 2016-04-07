# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import fnmatch
import logging.config
import os
import shutil

import pyinotify

from . import config as cfg
from .celery import app

logger = logging.getLogger(__name__)


def mkdir(path):
    if not os.path.exists(path):
        logger.debug('Creating directory %s', path)
        os.makedirs(path)
    else:
        assert(os.path.isdir(path))


def move(src, dst):
    logger.info('Moving %s to %s', src, dst)
    shutil.move(src, dst)


class FileHandler(pyinotify.ProcessEvent):
    """An event handler for new/updated files.

    Depending on the file extension, a task is sent to a task queue for further
    asynchronous processing. Only one task per file is sent, even in case of
    multiple matches.

    """
    def process_IN_CLOSE_WRITE(self, event):

        logger.info('Notified of %s', event.pathname)

        # Some setups require a file to be moved to a shared location first.

        if event.path in cfg.MOVES:
            src = event.pathname
            dst = cfg.MOVES[event.path]
            try:
                mkdir(dst)
                move(src, dst)
            except Exception as e:
                logger.error(e)
                return
            pathname = os.path.join(dst, event.name)
        else:
            pathname = event.pathname

        # Now that the file has been moved, notify the task server.

        for pattern in cfg.PATTERNS:
            if fnmatch.fnmatch(pathname.lower(), pattern):
                try:
                    taskname = cfg.PATTERNS[pattern]
                    logger.info('Sending task %s', taskname)
                    app.send_task(taskname, args=[pathname])
                except Exception as e:
                    logger.error(e)
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
    logging.config.dictConfig(cfg.LOGGING)
    notifier = get_notifier()
    notifier.loop()

if __name__ == '__main__':
    main()
