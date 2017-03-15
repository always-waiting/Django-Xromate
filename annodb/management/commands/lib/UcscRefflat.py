# encoding: utf-8

import annodb.models as dbmodels
import annodb.lib.parser as parser
from mongoengine import register_connection
from mongoengine.context_managers import switch_db

def importdb(cmdobj, **opt):
    """
    导入refflat.txt文件导入数据库，生成ucsc_refflat表
    """
    register_connection("cmd-import", opt['db'], opt['host'])
    refflat = parser.ParseRefFlat(opt['input'], opt['debug'])
    with switch_db(dbmodels.UcscRefflat, "cmd-import") as UcscRefflat:
        if opt['debug']: print "Deleting all data in database"
        UcscRefflat.objects.delete()
        if opt['debug']: print "Begin to insert new data into table ucsc_refflat"
        for genename, values in refflat.gene.iteritems():
            for one in values:
                refflat = UcscRefflat(**one)
                refflat.save()
