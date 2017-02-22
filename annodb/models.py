# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
import mongoengine as mongoe
from lib.OmimEntry import OmimEntry
from lib.DgvVarient import DgvVarient
from mysite.settings import DATABASES
# Create your models here.

mongoe.connect(DATABASES['annodb']['NAME'])

