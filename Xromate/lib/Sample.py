# encoding: utf-8
"""
Xromate系统sample表，用于记录样本信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring
from . import Flowcell
from . import Remote

class Samples(mongoe.Document):
    """
    collection name: sample
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }
    name = mongoe.StringField()
    interalresult = mongoe.StringField()
    lane = mongoe.DynamicField()
    index = mongoe.DynamicField()
    gender_choices = ['male', 'female']
    gender = mongoe.StringField(choices=gender_choices)
    summary = mongoe.DictField()
    result = mongoe.StringField()
    rejection = mongoe.StringField()
    auditor = mongoe.StringField()
    analyst = mongoe.StringField()
    state = mongoe.StringField() # 这个已经被result所代替,写上是为了以前的数据可用
    abstract = mongoe.StringField()
    state_desc = mongoe.StringField() # 这个已经被abstract所代替,写上是为了以前的数据可用
    description = mongoe.StringField()
    comment = mongoe.StringField() # 这个已经被description所代替,写上是为了以前的数据可用
    process_choices = ['unsubmitted','submitted', 'rejected', 'confirmed', 'synchronized']
    process = mongoe.StringField(choices=process_choices, default='unsubmitted')
    state_process = mongoe.StringField() # 这个已经被process所代替,写上是为了以前的数据可用
    images = mongoe.DictField() # 这个功能可以不用了，图片已经放到了一个目录下，没有存入数据库
    report = mongoe.DictField()
    submit_time = mongoe.DateTimeField()
    confirm_time = mongoe.DateTimeField()
    reject_time = mongoe.DateTimeField()
    sync_time = mongoe.DateTimeField()
    flowcell = mongoe.ReferenceField(Flowcell.Flowcells, dbref=True, reverse_delete_rule=2)
    remote = mongoe.ReferenceField(Remote.Remotes, dbref=True, reverse_delete_rule = 1)


    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)
