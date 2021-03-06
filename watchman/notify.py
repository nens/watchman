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
import time

import pyinotify

from . import config as cfg
from .celery import CONNECTION_POOLS
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


def uniquify(filename):
    """Make a filename unique by adding milliseconds since epoch.

    For example: foo.txt => foo@1596705456400.txt
    """
    root, ext = os.path.splitext(filename)  # foo.txt => ('foo', '.txt')
    ms = time.time() * 1000  # milliseconds since epoch as a float
    return "{root}@{ms:.0f}{ext}".format(root=root, ms=ms, ext=ext)

class FileHandler(pyinotify.ProcessEvent):
    """An event handler for new/updated files.

    Depending on the file extension, a task is sent to a task queue for further
    asynchronous processing. Only one task per file is sent, even in case of
    multiple matches.

    """
    ProFTPD = getattr(cfg, 'ProFTPD', False)

    def my_init(self, watch_manager={}):
        # The recommended way is not to override __init__ in your
        # subclass, but to define a my_init() method instead.
        # See pyinotify.ProcessEvent.
        self.wm = watch_manager

    def process_default(self, event):
        # If we are not watching directories created by ProFTPD,
        # return immediately.
        if not FileHandler.ProFTPD:
            return
        # Directory creation by ProFTPD is a two-step process. First a hidden
        # directory is created, e.g. `.dstXXX59N0g9`. Then, this directory
        # is renamed. This screws up the `auto_add` feature of pyinotify,
        # which automatically adds watches on newly created directories:
        # by the time pyinotify tries to add a watch, the dot folder
        # doesn't exist anymore, leaving the directory unwatched.
        if event.mask == pyinotify.IN_MOVED_TO | pyinotify.IN_ISDIR:
            if os.path.basename(event.src_pathname).startswith(".dst"):
                watches = {w.path: w for w in self.wm.watches.values()}
                parent_dir = os.path.dirname(event.pathname)
                parent_watch = watches.get(parent_dir)
                if (parent_watch and parent_watch.auto_add
                        and event.pathname not in watches):
                    self.wm.add_watch(
                        event.pathname, parent_watch.mask, auto_add=True)

    def process_IN_CLOSE_WRITE(self, event):

        logger.info('Notified of %s', event.pathname)

        # Some setups require a file to be moved to a shared location first.

        # If k = '/srv/ftp' and v = '/isilon/prod/data', then
        # '/srv/ftp/username/lizard/events.csv' will be moved to
        # '/isilon/prod/data/username/lizard/events@1596699866190.csv'.
        # The @milliseconds part is added to prevent filename clashes.

        pathname = event.pathname
        for k, v in cfg.MOVES.items():
            if event.pathname.startswith(k):
                src = event.pathname
                sub = event.path[len(k):].lstrip('/')
                dst = os.path.join(v, sub)
                try:
                    mkdir(dst)
                    mkdir(os.path.join(dst, 'accepted'))
                    mkdir(os.path.join(dst, 'rejected'))
                    filename = uniquify(event.name)
                    pathname = os.path.join(dst, filename)
                    move(src, pathname)
                except Exception as e:
                    logger.error(e)
                    return
                break

        # Now that the file has been moved, notify the task server.

        for pattern, data in cfg.PATTERNS.iteritems():
            if fnmatch.fnmatch(event.pathname, pattern):
                connection = None
                try:
                    task = data['task']
                    broker = data['broker']
                    kwargs = data.get('kwargs', {})
                    pool = CONNECTION_POOLS[broker]
                    connection = pool.acquire()
                    logger.info('Sending task %s', task)
                    app.send_task(task, args=[pathname], connection=connection, **kwargs)
                except Exception as e:
                    logger.error(e)
                finally:
                    if connection is not None:
                        connection.release()
                    break


def get_notifier():
    """Link directories being watched with an event handler.

    When a file that was opened for writing is closed, a FileHandler is
    notified.

    """
    wm = pyinotify.WatchManager()
    mask = pyinotify.ALL_EVENTS
    for watch in cfg.WATCHES:
        wm.add_watch(mask=mask, **watch)
    notifier = pyinotify.Notifier(wm, FileHandler(watch_manager=wm))
    return notifier


def main():
    logging.config.dictConfig(cfg.LOGGING)
    notifier = get_notifier()
    notifier.loop()

if __name__ == '__main__':
    main()
