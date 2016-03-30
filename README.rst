watchman
==========================================

Watch directories for new files and send tasks to a queue for futher
asynchronous processing.


Building watchman
-----------------

::

    git clone git@github.com:nens/watchman.git
    cd watchman
    ln -s profiles/development.cfg buildout.cfg
    python bootstrap.py
    bin/buildout


Configuring watchman
--------------------

Firstly, copy celeryconfig-example.py to celeryconfig.py and configure the
location of your Celery broker, for example::

    BROKER_URL = "redis://localhost:6379/0"

Secondly, copy config-example.py to config.py and configure logging and
pyinotify.

WATCHES lists the directories to monitor for new files::

    WATCHES = [
        {'path': '/foo'},
        {'path': '/bar', 'rec': True},  # watch subdirectories too
    ]

PATTERNS maps file extensions on Celery tasks::

    PATTERNS = {
        '*': 'proj.tasks.echo',
    }

Sometimes order matters::

    PATTERNS = OrderedDict([
        ('*/events/*.csv', 'proj.tasks.import_events'),
        ('*.csv', 'proj.tasks.import_timeseries'),
    ])

New files may be moved to another location (e.g. permanent storage) before
submitting tasks. This is optional::

    MOVES = {
        '/foo': '/isilon/foo',
    }


Running watchman
----------------

Interactively::

    bin/notify

Daemonized::

    bin/supervisord
