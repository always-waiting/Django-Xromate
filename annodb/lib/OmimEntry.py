# encoding: utf-8
"""
在这里定义参考数据库的omim_entry表
"""
from __future__ import unicode_literals
from django.db import models
import mongoengine as mongoe
import re
from annodb.apps import AnnodbConfig, dumpstring

class OmimEntry(mongoe.Document):
    """
    collection name: omim_entry
    """
    #meta = {'db_alias': DATABASES['annodb']['alias']}
    meta = {'db_alias': AnnodbConfig.alias}

    prefix_choices = ('*', '+', '#', '%', '^', '','1','2','3','4','5','6')
    prefix = mongoe.StringField(max_length=3, choices=prefix_choices)
    mimNumber = mongoe.IntField()
    title = mongoe.DictField()
    status_choices = ('live', 'moved', 'removed')
    status = mongoe.StringField(max_length=10, choices=status_choices, default='live')
    movedTo = mongoe.IntField()
    # perl中没有规定类型
    geneMapExists = mongoe.BooleanField()
    geneMap = mongoe.DictField()
    # perl中没有规定类型
    phenotypeMapExists = mongoe.BooleanField()
    phenotypeMapList = mongoe.ListField()
    textSectionList = mongoe.ListField(mongoe.DictField())
    # perl中没有规定类型
    clinicalSynopsisExists = mongoe.BooleanField()
    clinicalSynopsisList = mongoe.DictField()
    # 自行添加的内容
    allelicVariantExists = mongoe.BooleanField()
    allelicVariantList = mongoe.DictField()
    # 少类型检查
    allelicVariantList = mongoe.ListField(mongoe.DictField())
    seeAlso = mongoe.StringField()
    # 少类型检查
    referenceList = mongoe.ListField(mongoe.DictField())
    clinicalSynopsis = mongoe.DictField()
    contributors = mongoe.StringField()
    editHistory = mongoe.StringField()
    createDate = mongoe.StringField()
    """
    以下是没有定义的属性
    creationDate
    dateCreated
    epochCreated
    dateUpdated
    epochUpdated
    """
    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

