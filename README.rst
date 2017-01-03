watchman
========

Watch directories for new files and send tasks to a queue for further
asynchronous processing. This project is deliberately lightweight
(simple configuration via files, no database and/or web server).
We use watchman on our FTP server to automatically process
uploaded files.


Building watchman
-----------------

Development with Vagrant, virtualenv, etc::

    $ git clone git@github.com:nens/watchman.git
    $ cd watchman
    $ ln -s profiles/development.cfg buildout.cfg
    $ python bootstrap.py
    $ bin/buildout

Development with Docker::

    $ git clone git@github.com:nens/watchman.git
    $ cd watchman
    $ ln -s profiles/development.cfg buildout.cfg
    $ docker-compose build
    $ docker volume create --name=ftproot
    $ docker-compose run --rm watchman python bootstrap.py
    $ docker-compose run --rm watchman bin/buildout

NB: We share the volume `ftproot` with another Docker project. Adjust to your
needs.


Configuring watchman
--------------------

Firstly, create a celeryconfig.py and configure Celery as desired,
for example::

    CELERYD_HIJACK_ROOT_LOGGER = False

By default, tasks are sent to a queue named "celery". If a task needs to be
routed to a specific queue, this may be done as follows::

    CELERY_ROUTES = {
        'lizard_nxt.tasks.import_raster_task': {'queue': 'single_worker'},
    }

NB: Celery v4 uses new lowercase settings. Check out the documentation.

Since multiple brokers are supported, do not define a `BROKER_URL` here as you
would typically do when working with Celery. (NB: This setting supports a
list of broker URLs, but this is for use in a failover strategy.)

Secondly, copy config-example.py to config.py and configure logging and
pyinotify.

If watchman is used to recursively watch directories created by
ProFTPD, use this setting::

    ProFTPD = True

Without this setting, Pyinotify's feature to recursively watch
newly created directories doesn't function properly.

Configure one or more brokers::

    BROKERS = {
        'lizard': 'amqp://guest:guest@rabbitmq:5672//',
        '3di': 'redis://redis:6379/0',
    }

WATCHES lists the directories to monitor for new files::

    WATCHES = [
        {'path': '/srv/ftp', 'rec': True, 'auto_add': True},
    ]

See WatchManager's add_watch function: http://seb-m.github.io/pyinotify/.

PATTERNS maps file extensions on Celery tasks::

    PATTERNS = {
        ('/srv/ftp/*.csv', {'broker': 'lizard', 'task': 'lizard_task'}),
        ('/srv/ftp/*.nc', {'broker': '3di', 'task': '3di_task'}),
    }

See fnmatch: https://docs.python.org/2/library/fnmatch.html.

Sometimes order matters (most specific first)::

    PATTERNS = OrderedDict([
        ('/srv/ftp/*/events/*.csv', {'broker': 'lizard', 'task': 'process_events'}),
        ('/srv/ftp/*.csv', {'broker': 'lizard', 'task': 'process_timeseries'}),
    ])

New files may be moved to another location (e.g. permanent storage) before
submitting tasks. This is optional (you may leave this dictionary empty)::

    MOVES = {
        '/srv/ftp': '/isilon/foo/bar',
    }

This will move /srv/ftp/username/lizard/events.csv to
/isilon/foo/bar/username/lizard/events.csv before sending the task.

Running watchman
----------------

Interactively::

    $ bin/notify

Daemonized::

    $ bin/supervisord

Development with docker::

    $ docker-compose up

Verify that it works::

    $ docker exec -it watchman_watchman_1 /bin/bash
    $ cd /srv/ftp
    $ touch data.csv

The log window should display something like this::

    watchman_1  | 2016-12-28 16:17:13,803 [INFO] watchman.notify: Notified of /srv/ftp/data.csv
    watchman_1  | 2016-12-28 16:17:13,827 [INFO] watchman.notify: Sending task lizard_task

Visit the RabbitMQ management interface in your browser and inspect the celery queue::

    http://localhost:15672/#/queues
