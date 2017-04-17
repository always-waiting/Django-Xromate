# encoding:utf-8
"""
Xromate系统Logs表,用于记录处理的log
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring
from . import Sample
from . import CNV
import json

class Logs(mongoe.Document):
    """
    collection name: logs
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }

    time = mongoe.IntField()
    comment = mongoe.StringField()
    user = mongoe.StringField()
    operation = mongoe.StringField(choices=['submit','confirm','reject'])

    result = mongoe.StringField()
    abstract = mongoe.StringField()
    location = mongoe.StringField()
    description = mongoe.StringField()

    sample = mongoe.ReferenceField(Sample.Samples, dbref=True, reverse_delete_rule=2)
    cnv = mongoe.ReferenceField(CNV.Cnvs, dbref=True, reverse_delete_rule=2)

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)
