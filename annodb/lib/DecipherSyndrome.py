# encoding: utf-8
"""
这里定义注释数据库的decipher_syndrome表
"""

import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class DecipherSyndrome(mongoe.Document):
    """
    collection name: decipher_syndrome
    """
    meta = {
        'db_alias': AnnodbConfig.alias,
    }

    syndrome_id = mongoe.IntField()
    copy_number = mongoe.IntField()
    start = mongoe.IntField()
    end = mongoe.IntField()
    no_id = mongoe.IntField()
    chr = mongoe.StringField()
    short_description = mongoe.StringField()
    assembly = mongoe.StringField()
    grch37_position = mongoe.StringField()
    remap_value = mongoe.StringField()
    remapped_from = mongoe.StringField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)
