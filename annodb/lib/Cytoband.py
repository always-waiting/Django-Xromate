#encoding: utf-8
"""
注释数据库的cytoband表
"""
import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class Cytoband(mongoe.Document):
    """
    collection name: cytoband
    """
    meta = {
        'db_alias': AnnodbConfig.alias,
    }

    description  = mongoe.StringField()
    name = mongoe.StringField()
    chr = mongoe.StringField()
    chrom = mongoe.StringField()
    start = mongoe.IntField()
    end = mongoe.IntField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

