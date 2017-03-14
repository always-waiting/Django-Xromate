#encoding: utf-8
"""
注释数据库的pubmed表
"""
import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class Pubmed(mongoe.Document):
    """
    collection name: pubmed
    """
    meta = {
        'db_alias': AnnodbConfig.alias,
    }
    gainloss = mongoe.StringField()
    description = mongoe.StringField()
    cytoband = mongoe.StringField()
    size = mongoe.StringField()
    origin_position = mongoe.StringField()
    critical = mongoe.StringField()
    hg_ver = mongoe.StringField()
    inheritance = mongoe.StringField()
    note = mongoe.StringField()
    extra_desc = mongoe.StringField()
    auditor  = mongoe.StringField()
    comment = mongoe.StringField()
    chr = mongoe.StringField()

    have_fulltext = mongoe.BooleanField()

    gender = mongoe.IntField()
    start = mongoe.IntField()
    end = mongoe.IntField()

    pmid = mongoe.ListField()
    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

