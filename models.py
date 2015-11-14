"""
Models and database for wcycle application
"""

import os
from playhouse.db_url import connect
from peewee import Model as _Model, CharField, DateField, IntegerField

# Database settings
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'db.sqlite3'
DB_PATH = os.path.abspath(os.path.join(PROJECT_ROOT, DB_NAME))
DB_URL = 'sqlite:///%s' % DB_PATH

db = connect(DB_URL)


class Model(_Model):
    class Meta:
        database = db


WC_STABILITY_STABLE = 0
WC_STABILITY_UNSTABLE = 1
WC_STABILITY_CHOICES = (
    (WC_STABILITY_STABLE, 'Stable'),
    (WC_STABILITY_UNSTABLE, 'Unstable')
)


class Woman(Model):
    full_name = CharField(max_length=255, verbose_name='Full name')
    wc_stability = IntegerField(choices=WC_STABILITY_CHOICES, verbose_name='Stability')
    wc_last_cycle = DateField(verbose_name='Last cycle')
    wc_cycle = IntegerField(verbose_name='Cycle in days')


if not os.path.exists(DB_PATH):
    db.create_tables([Woman])
