#encoding: utf-8
"""
注释数据库的clin_var表
"""
import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class ClinVar(mongoe.Document):
    """
    collection name: clin_var
    """
    meta = {
        'db_alias': AnnodbConfig.alias,
    }
    type = mongoe.StringField()
    name = mongoe.StringField()
    rcv_accession = mongoe.StringField()
    clinsign = mongoe.StringField()
    origin = mongoe.StringField()
    assembly = mongoe.StringField()
    chrchr = mongoe.StringField()
    cytogenetic = mongoe.StringField()
    date_update = mongoe.StringField()
    pubmeds  = mongoe.StringField()
    gene_reviews = mongoe.StringField()
    chr = mongoe.StringField()
    allele_id = mongoe.IntField()
    start = mongoe.IntField()
    end = mongoe.IntField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

