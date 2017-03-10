# encoding: utf-8

import annodb.models as dbmodels
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
import annodb.lib.parser as parser

def importdb(cmdobj, **opt):
    """
    导入GeneReview数据库
    只导入accession，gene_symbol，description三个字段
    """
    print "开发"
    register_connection("cmd-import", opt['db'], opt['host'])
    url = "ftp.ncbi.nih.gov"
    path = "pub/GeneReviews/"
    filename = "GRshortname_NBKid_genesymbol_dzname.txt"
    GRparser = parser.ParseGeneReview(url, path, filename, opt['debug'], opt['nthread'])
    itervalue = iter(GRparser)
    if opt['test']:
        pass
    else:
        if opt['debug']: print "删除数据库原有信息"
        with switch_db(dbmodels.GeneReview, "cmd-import") as GeneReview:
            GeneReview.objects.delete()
            for one in itervalue:
                gene = GeneReview(**one)
                gene.save()

