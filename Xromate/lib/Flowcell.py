# encoding: utf-8
"""
Xromate系统flowcell表，用于记录批次信息信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring

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

