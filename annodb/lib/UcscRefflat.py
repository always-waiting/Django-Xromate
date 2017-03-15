# encoding: utf-8
"""
注释数据库ucsc_reffalt
"""

import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class UcscRefflat(mongoe.Document):
    """
    colleciton name: ucsc_refflat
    """
    meta = {
        'db_alias': AnnodbConfig.alias
    }

    geneName = mongoe.StringField()
    name = mongoe.StringField()
    chrom = mongoe.StringField()
    strand = mongoe.StringField()

    txStart = mongoe.IntField()
    txEnd = mongoe.IntField()
    cdsStart = mongoe.IntField()
    cdsEnd = mongoe.IntField()
    exonCount = mongoe.IntField()

    exonStarts = mongoe.ListField()
    exonEnds = mongoe.ListField()
    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

