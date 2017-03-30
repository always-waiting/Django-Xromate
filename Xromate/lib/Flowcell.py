# encoding: utf-8
"""
Xromate系统flowcell表，用于记录批次信息信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring
import datetime
#from . import Sample

class Flowcells(mongoe.Document):
    """
    collection name: flowcell
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }

    name = mongoe.StringField()
    project = mongoe.StringField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

    def newflag(self):
        timenow = datetime.datetime.now()
        day = (timenow - self.id.generation_time.replace(tzinfo=None)).days
        if day < 7:
            return 1
        else:
            return 0
    newtag = property(newflag)

    #samples = mongoe.ListField(mongoe.EmbeddedDocumentField(Sample.Samples))
