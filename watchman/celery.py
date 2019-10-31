# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from celery import Celery
from kombu.connection import Connection

from . import celeryconfig
from . import config

app = Celery()
app.config_from_object(celeryconfig, namespace="CELERY")

CONNECTION_POOLS = {
    broker_name: Connection(broker_url).ChannelPool()
    for broker_name, broker_url
    in config.BROKERS.items()
}
