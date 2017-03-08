# encoding: utf-8
"""
这里定义注释数据库的decipher_cnv表
"""

import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class DecipherCnv(mongoe.Document):
    """
    collection name: decipher_cnv
    """
    meta = {
        'db_alias': AnnodbConfig.alias,
    }

    patient_id = mongoe.IntField()
    project_id = mongoe.IntField()
    no_id = mongoe.IntField()
    #id = mongoe.IntField()
    #_id = mongoe.ObjectIdField(db_field="_id")
    user_id = mongoe.IntField()
    start = mongoe.IntField()
    end = mongoe.IntField()
    mean_ratio = mongoe.FloatField()
    inheritance = mongoe.StringField()
    pathogenicity = mongoe.StringField()
    phenotypes = mongoe.StringField()
    chr_sex = mongoe.StringField()
    assembly = mongoe.StringField()
    grch37_position = mongoe.StringField()
    remap_value = mongoe.StringField()
    chr = mongoe.StringField()
    remapped_from = mongoe.StringField()


    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)
