# encoding: utf-8
import os
import re
import annodb.models as dbmodels
import annodb.lib.parser as parser
import mongoengine

#print "2"*60
#dbmodels.dbconnection('test', 'mongodb://192.168.4.13:27017')
def test():
    print u"这时一个测试，用于判断是否成功加载"

def omim_entry_import(cmdobj, **options):
    u"""
    导入omim.txt到数据库
    """
    # 检查文件是否存在
    if not os.path.exists(options['input']):
        raise Exception(options['input'] + " not exists");
    # 检查能否链接数据库
    try:
        mongoengine.register_connection("cmd-omimentry-import", options['db'], options['host'])
    except:
        raise Exception(u"链接数据库" + options['host'] + "/" + options['db']+ u"失败")
    with open(options['input']) as f:
        for chunk in parser.myreadlines(f, '*RECORD*'):
            if not chunk: continue;
            if chunk.find("*THEEND*") != -1: break
            #if chunk.find('104760') != -1:
            entryone = parser.ParseEntry(chunk);
            import_omim_entry(entryone.record)


def import_omim_entry(record):
    with mongoengine.context_managers.switch_db(dbmodels.OmimEntry, "cmd-omimentry-import") as dbmodels.OmimEntry:
        try:
            entry = dbmodels.OmimEntry.objects.get(mimNumber = record['mimNumber'])
            entry.update(**record)
        except dbmodels.OmimEntry.DoesNotExist:
            entry = dbmodels.OmimEntry(**record)
        except dbmodels.OmimEntry.MultipleObjectsReturned:
            raise Exception(u"有多条记录，需要人工核查!")
        except:
            raise Exception(u"在数据库查询时出现未知错误")
        entry.save()

