# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
import mongoengine as mongoe
from lib.OmimEntry import OmimEntry
from lib.DgvVarient import DgvVarient
from lib.OmimGenemap import OmimGenemap
from lib.OmimMorbidmap import OmimMorbidmap
from lib.DecipherCNV import DecipherCnv
from lib.DecipherSyndrome import DecipherSyndrome
from apps import AnnodbConfig
# Create your models here.

'''
from mysite.settings import DATABASES
mongoe.connect(
    DATABASES['annodb']['NAME'],
    host=DATABASES['annodb']['HOST'],
    alias=DATABASES['annodb']['alias']
)
'''
mongoe.connect(
    AnnodbConfig.db,
    host=AnnodbConfig.host,
    alias=AnnodbConfig.alias
)

def dbconnection(dbname, host='mongodb://localhost:27017', alias='annodb'):
    """
    这个函数已经可以删除了，没有用处了
    """
    try:
        mongoe.connect(dbname, host=host, alias=alias)
    except:
        raise Exception(u"数据库链接失败")

