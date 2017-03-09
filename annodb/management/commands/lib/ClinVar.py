# encoding: utf-8

import annodb.models as dbmodels
import annodb.lib.parser as parser
from mongoengine import register_connection
from mongoengine.context_managers import switch_db

def importdb(cmdobj, **opt):
    """
    导入ClinVarFullRelease.xml文件到数据库
    """
    register_connection("cmd-import", opt['db'], opt['host'])
    with switch_db(dbmodels.ClinVar, "cmd-import") as ClinVar:
        ClinVar.objects.delete()
        with parser.ParseClinVar(opt['input'], opt['debug']) as parseclinvar:
            for one in parseclinvar:
                if len(one.keys()):
                    clinvar = ClinVar(**one)
                    clinvar.save()
