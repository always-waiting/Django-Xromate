# encoding: utf-8


import annodb.models as dbmodels
import annodb.lib.parser as parser
from mongoengine import register_connection
from mongoengine.context_managers import switch_db

def importdb(cmdobj, **opt):
    """
    通过输入文件，导入样本到pubmed表
    """
    register_connection("cmd-import", opt['db'], opt['host'])
    parsefile = parser.ParsePubmed(opt['input'],opt['debug'])
    data = parsefile.generate_data()
    with switch_db(dbmodels.Pubmed, "cmd-import") as Pubmed:
        Pubmed.objects.delete()
        for item in data:
            pubmed = Pubmed(**item)
            pubmed.save()

