# encoding:utf8
"""
Xromate系统mcc表，用于记录mcc信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring
from . import Flowcell
from . import User
import datetime

class Mccs(mongoe.Document):
    """
    collection name: mcc
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }
    prediction = mongoe.StringField()
    name = mongoe.StringField()
    analyst = mongoe.StringField()
    auditor = mongoe.StringField()
    quality = mongoe.StringField()
    process = mongoe.StringField(choices=['unanalyzed', 'analyzed', 'rejected', 'confirmed', 'synchronized'], default='unanalyzed')
    result = mongoe.StringField()
    analyze_time = mongoe.DateTimeField()
    confirm_time = mongoe.DateTimeField()
    sync_time = mongoe.DateTimeField()
    reject_time = mongoe.DateTimeField()
    flowcell = mongoe.ReferenceField(Flowcell.Flowcells, dbref=True, reverse_delete_rule=2)
    images = mongoe.DictField() # 以后这个就不会用了，现在为了以前数据的兼容
    rejection = mongoe.StringField()
    annotation = mongoe.StringField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

    def analyst_as_text(self):
        try:
            user = User.Users.objects.get(username=self.analyst)
            return user.name
        except User.Users.DoesNotExist:
            return ''

    def handle_time(self):
        if self.process == 'unanalyzed':
            return ''
        elif self.process == 'analyzed':
            return self.analyze_time
        elif self.process == 'rejected':
            return self.reject_time
        elif self.process == 'confirmed':
            return self.confirm_time
        elif self.process == 'synchronized':
            return self.sync_time
        else:
            return ''




