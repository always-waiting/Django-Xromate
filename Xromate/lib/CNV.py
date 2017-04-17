# encoding:utf8
"""
Xromate系统cnv表，用于记录cnv信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring
import datetime
from . import Sample

class Cnvs(mongoe.Document):
    """
    collection name: cnvs
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }
    chr = mongoe.StringField()
    start = mongoe.IntField()
    end = mongoe.IntField()
    blockStart = mongoe.IntField()
    blockEnd = mongoe.IntField()
    blockNA = mongoe.IntField()
    copy = mongoe.DecimalField()
    mosaic = mongoe.StringField()
    log2 = mongoe.DecimalField()
    zvalue = mongoe.DecimalField()
    gainloss = mongoe.StringField(choices=['gain', 'loss'])
    type = mongoe.StringField()
    result = mongoe.StringField(choices=['normal','polymorphism','unknown','exception','mosaic','monosome','disome','trisome','tetrasome','triploid','tetraploid','other'])
    abstract = mongoe.StringField()
    rejection = mongoe.StringField()
    description = mongoe.StringField()
    process = mongoe.StringField(choices=['unsubmitted','submitted','confirmed','deleted','rejected'],default='unsubmitted')
    source = mongoe.StringField(choices=['imported','created','merged'],default='imported')
    cytoband = mongoe.StringField()
    sample = mongoe.ReferenceField(Sample.Samples, dbref=True, reverse_delete_rule=2)
    state = mongoe.StringField()
    auditor = mongoe.StringField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

    def search_logs(self, **opt):
        from . import Log
        logsqueryset = Log.Logs.objects(__raw__={'cnv.$id': self.id}, **opt)
        return logsqueryset
