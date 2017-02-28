# encoding: utf-8
"""
这里定义注释数据库的omim_genemap表
"""

from __future__ import unicode_literals
from django.db import models
import mongoengine as mongoe
import re
from annodb.apps import AnnodbConfig, dumpstring

class OmimGenemap(mongoe.Document):
    """
    collection name: omim_genemap
    """
    meta = {'db_alias': AnnodbConfig.alias}

    sequenceID = mongoe.IntField()
    chromosome = mongoe.IntField()
    chromosomeSymbol = mongoe.StringField()
    #chromosomeSort = mongoe.IntField()# 这个属性应该没有用处
    # mim2gene_update处理
    approvedGeneSymbol = mongoe.StringField()
    chromosomeLocationStrand = mongoe.StringField()
    chromosomeLocationStart = mongoe.IntField()
    chromosomeLocationEnd = mongoe.IntField()
    # done
    #transcript = mongoe.StringField()# 这个属性应该没有用处
    cytoLocation = mongoe.StringField()
    #computedCytoLocation = mongoe.StringField() # 这个属性应该没有用处
    mimNumber = mongoe.IntField()
    geneSymbols = mongoe.StringField()
    #geneName = mongoe.StringField()# 这个属性应该没有用处
    mappingMethod = mongoe.StringField()
    #confidence = mongoe.StringField(max_length=3, choices=('P', 'L'))# perl中为L应该是错误
    #confidence = mongoe.StringField(max_length=3, choices=('P', 'C'))
    confidence = mongoe.StringField()
    geneInheritance = mongoe.StringField()
    phenotypeMapList = mongoe.ListField(mongoe.DictField())
    # 以下是perl中没有的
    title = mongoe.StringField()
    disorders = mongoe.StringField()
    comments = mongoe.StringField()
    mouseGeneSymbol = mongoe.StringField()
    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

