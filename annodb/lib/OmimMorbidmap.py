#encoding: utf-8
"""
这里定义注释数据库的omim_morbidmap表
"""

import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class OmimMorbidmap(mongoe.Document):
    """
    collection name: omim_morbidmap
    chr, start, ent由cytoband表更新获得，这个以后处理
    """
    meta = {'db_alias': AnnodbConfig.alias}

    phenotypeMimNumber = mongoe.IntField()
    chr = mongoe.StringField()
    start = mongoe.IntField()
    end = mongoe.IntField()
    cytoLocation = mongoe.StringField()
    mimNumber = mongoe.IntField()
    geneSymbols = mongoe.StringField()
    phenotype = mongoe.StringField()
    phenotypeMappingKey = mongoe.IntField()
    geneMapExists = mongoe.BooleanField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

