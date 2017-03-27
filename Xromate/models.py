from __future__ import unicode_literals

from django.db import models
import mongoengine as mongoe
from lib.User import User
from apps import XromateConfig
# Create your models here.

mongoe.connect(
    XromateConfig.db,
    host=XromateConfig.host,
    alias=XromateConfig.alias
)
