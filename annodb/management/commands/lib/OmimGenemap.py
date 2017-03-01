# encoding: utf-8
import os
import re
import annodb.models as dbmodels
import annodb.lib.parser as parser
#from annodb.models import OmimGenemap,OmimEntry
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
#import mongoengine
from contextlib import nested
import json

def mim2gene_update(cmdobj, **opt):
    """
    通过mim2gene.txt和refFlat.txt文件更新Genemap表
    """
    # 检查文件
    if not os.path.exists(opt['input']):
        raise Exception(opt['input'] + " not exists")
    if not os.path.exists(opt['refflat']):
        raise Exception(opt['refflat'] + " not exists")
    try:
        register_connection("cmd-mim2gene_update", opt['db'], opt['host'])
    except:
        raise Exception("数据库链接失败")
    # 解析refFlat
    refFlat = parser.ParseRefFlat(opt['refflat'])
    with switch_db(dbmodels.OmimGenemap,'cmd-mim2gene_update') as OmimGenemap:
        with open(opt['input']) as f:
            for line in f:
                line = line.lstrip().rstrip()
                if not line: continue
                if line.startswith("#"): continue
                record = parser.ParseMim2gene(line);
                if record.approvedGeneSymbol:
                    symbol = record.approvedGeneSymbol
                else:
                    print "OMIM", record.mimNumber,"is",record.type
                    continue
                if not refFlat.gene.has_key(symbol): continue
                changes = refFlat.make_changes(symbol)
                mim = record.mimNumber
                try:
                    genemap = OmimGenemap.objects.get(mimNumber = int(mim))
                except OmimGenemap.DoesNotExist:
                    print "在",opt['host'],"/",opt['db'],"/omim_genemap中没有",mim
                    continue
                except OmimGenemap.MultipleObjectsReturned:
                    print "在",opt['host'],"/",opt['db'],"/omim_genemap中有多个",mim
                    continue
                genemap.update(**changes)
                genemap.save()

def omim_genemap_update_entry(cmdobj, **options):
    '''
    通过mimNumber把omim_genemap的信息更新到omim_entry
    '''
    try:
        register_connection("cmd-update-subject", options['genemapdb'], options['genemaphost'])
        register_connection("cmd-update-object", options['entrydb'], options['entryhost'])
    except:
        raise Exception("链接数据库失败")
    with switch_db(dbmodels.OmimGenemap, "cmd-update-subject") as OmimGenemap:
        with switch_db(dbmodels.OmimEntry, "cmd-update-object") as OmimEntry:
            objlist = []
            if options['mimNumber']:
                for mim in options['mimNumber']:
                    try:
                        genemap = OmimGenemap.objects.get(mimNumber = int(mim))
                        objlist.append(genemap)
                    except OmimGenemap.DoesNotExist:
                        print "".join(["在",options['genemaphost'],"/",options['genemapdb'],"/omim_genemap中没有",mim])
                        continue
                    except OmimGenemap.MultipleObjectsReturned:
                        print "".join(["在",options['genemaphost'],"/",options['genemapdb'],"/omim_genemap中有多个",mim])
                        continue
            else:
                objlist = OmimGenemap.objects
            for genemap in objlist:
                record = json.loads(genemap.to_json())
                record.pop("_id")
                try:
                    entry = OmimEntry.objects.get(mimNumber = genemap.mimNumber)
                    upsertrecord = {'geneMapExists': True, 'geneMap': record}
                    entry.update(**upsertrecord)
                    entry.save()
                except OmimEntry.DoesNotExist:
                    print "".join(["在omim_entry中查询",str(genemap.mimNumber),"不存在"])
                    continue
                except OmimEntry.MultipleObjectsReturned:
                    print "".join(["在omim_entry中查询",str(genemap.mimNumber),"有多个"])
                    continue

def omim_genemap_import(cmdobj, **options):
    """
    导入genemap.txt到数据库
    """
    if not os.path.exists(options['input']):
        raise Exception(options['input'] + " not exists")
    try:
        register_connection("cmd-import", options['db'], options['host'])
    except:
        raise Exception(options['host']+'/'+options['db']+"链接失败")
    with open(options['input']) as f:
        for chunk in f:
            chunk = chunk.lstrip().rstrip()
            if chunk.startswith("#"): continue
            if not chunk: continue
            genemapone = parser.ParseGenemap(chunk)
            import_omim_genemap(genemapone.record)

def import_omim_genemap(record):
    with switch_db(dbmodels.OmimGenemap, "cmd-import") as OmimGenemap:
        try:
            genemap = OmimGenemap.objects.get(mimNumber = record['mimNumber'])
            genemap.update(**record)
        except OmimGenemap.DoesNotExist:
            genemap = OmimGenemap(**record)
        except OmimGenemap.MultipleObjectsReturned:
            raise Exception("有多条记录，需要人工核查!")
        except:
            raise Exception("在数据库查询时出现未知错误")
        genemap.save()
