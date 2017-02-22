# encoding: utf-8
"""
在这里定义参考数据库的omim_entry表
"""
from __future__ import unicode_literals
from django.db import models
import mongoengine as mongoe
import re

class OmimEntry(mongoe.Document):
    """
    collection name: omim_entry
    """
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

def dumpstring(obj, newline="\n", space="\t", level=0):
    string = []
    if type(obj) == dict:
        string.append("%s{%s" % (level*space, newline))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                string.append("%s%s =>%s" % ((level+1)*space, k, newline))
                string.append(dumpstring(v, level = level+1))
            else:
                string.append("%s%s => %s%s" % ((level+1)*space, k, v, newline))
        string.append("%s}%s" % (level*space, newline))
    elif type(obj) == list:
        string.append("%s[%s" % (level*space, newline))
        for v in obj:
            if hasattr(v, '__iter__'):
                string.append(dumpstring(v, level = level+1))
            else:
                string.append("%s%s%s" % ((level+1)*space, v, newline))
        string.append("%s]%s" % (level*space, newline))
    else:
        strobj = str(obj)
        addlevelobj = re.sub("\n","\n"+level*space, strobj)
        string.append("%s%s%s" % (level*space, addlevelobj, newline))
    return "".join(string)



