# encoding: utf-8
import os
import re
import annodb.models as dbmodels
#from annodb.models import OmimGenemap,OmimEntry
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
#import mongoengine
from contextlib import nested

def omim_genemap_import(cmdobj, **options):
    u"""
    导入genemap.txt到数据库
    """
    print u"开发omim_genemap_import命令".encode("utf-8")
    if not os.path.exists(options['input']):
        raise Exception(options['input'] + " not exists")
    try:
        register_connection("cmd-import", options['db'], options['host'])
    except:
        raise Exception(options['host']+'/'+options['db']+u"链接失败")
    with open(options['input']) as f:
        for chunk in f:
            chunk = chunk.lstrip().rstrip()
            if chunk.startswith("#"): continue
            if not chunk: continue
            #print chunk
            # 解析记录
            record = parser_genemap(chunk)
            # 插入到数据库
            import_omim_genemap(record)

def import_omim_genemap(record):
    #with context_managers.switch_db(OmimGenemap, "cmd-import") as OmimGenemap:
    #    with context_managers.switch_db(OmimEntry, "cmd-import") as OmimEntry:
    #        print OmimEntry # 报错由于名字相同，所以出错，as后不同名即可
    with switch_db(dbmodels.OmimGenemap, "cmd-import") as OmimGenemap:
        with switch_db(dbmodels.OmimEntry, "cmd-import") as OmimEntry:
            try:
                genemap = OmimGenemap.objects.get(mimNumber = record['mimNumber'])
                genemap.update(**record)
            except OmimGenemap.DoesNotExist:
                genemap = OmimGenemap(**record)
            except OmimGenemap.MultipleObjectsReturned:
                raise Exception(u"有多条记录，需要人工核查!")
            except:
                raise Exception(u"在数据库查询时出现未知错误")
            genemap.save()
            # 处理omim_entry表
            try:
                entry = OmimEntry.objects.get(mimNumber = record['mimNumber'])
                #print "Find"+str(record['mimNumber'])
                try:
                    upsertrecord = {
                        'geneMapExists': True,
                        'geneMap': record
                    }
                    entry.update(**upsertrecord)
                    entry.save()
                except Exception, e:
                    print e
                    raise Exception(u"导入genemap.txt时，修改omim_entry出错")
            except OmimEntry.DoesNotExist:
                print u"导入genemap.txt时，在omim_entry中查询"+str(record['mimNumber'])+u"不存在"
                return
            except OmimEntry.MultipleObjectsReturned:
                raise Exception(u"导入genemap.txt时，在omim_entry中查询"+str(record['mimNumber'])+u"有过个结果")
            except:
                raise Exception(u"导入genemap.txt时，在omim_entry中查询出现未知错误")
def parser_genemap(chunk):
    item = chunk.split("\t")
    (chrnum, seqid) = item[0].split(".")
    chr_symbols = list(range(23))
    chr_symbols.extend(["X","Y"])
    genemap = {
        'chromosome': int(chrnum),
        'chromosomeSymbol': str(chr_symbols[int(chrnum)]),
        'sequenceID': int(seqid)
    }
    headers = 'month day year cytoLocation geneSymbols confidence \
        title mimNumber mappingMethod comments disorders \
        mouseGeneSymbol references'.split()
    for i in range(len(headers)):
        try:
            if headers[i] == "mimNumber":
                genemap[headers[i]] = int(item[i+1])
            elif headers[i] == 'confidence':
                genemap[headers[i]] = item[i+1].upper()
            elif re.search("month|day|year",headers[i]):
                continue
            else:
                genemap[headers[i]] = item[i+1]
        except IndexError:
            pass
        except:
            raise Exception(u"在解析genemap.txt时发生未知错误")
    #print len(item)
    #print genemap
    return genemap

