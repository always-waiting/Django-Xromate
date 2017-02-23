from __future__ import unicode_literals

from django.apps import AppConfig


class AnnodbConfig(AppConfig):
    name = 'annodb'
    db = 'annodb'
    host = "mongodb://localhost:27017"
    alias = 'default'
