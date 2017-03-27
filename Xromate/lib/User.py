# encoding:utf-8
"""
Xromate系统user表,用于记录xromate系统的用户信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring

class User(mongoe.Document):
    """
    collection name: user
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }
    username = mongoe.StringField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

