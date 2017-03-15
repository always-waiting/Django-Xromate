# encoding: utf-8

import annodb.models as dbmodels
import annodb.lib.parser as parser
from mongoengine import register_connection
from mongoengine.context_managers import switch_db

def importdb(cmdobj, **opt):
    """
    导入cytoband.txt文件，存储cytoband信息
    """
    register_connection("cmd-import", opt['db'], opt['host'])
    cytobandinfo = parser.ParseCytoband(opt['input'], opt['debug'])
    with switch_db(dbmodels.Cytoband, "cmd-import") as Cytoband:
        if opt['debug']: print "Deleting all old cytoband"
        Cytoband.objects.delete()
        if opt['debug']: print "Insert all cytoband"
        for cyto in cytobandinfo.cytobands:
            Cytoband(**cyto).save()
