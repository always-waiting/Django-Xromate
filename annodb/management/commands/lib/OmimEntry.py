# encoding: utf-8
import os
import re
import json
from bs4 import BeautifulSoup
import annodb.models as dbmodels
import urllib3
import annodb.lib.parser as parser
from mongoengine import register_connection
from mongoengine.context_managers import switch_db

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
        register_connection("cmd-omimentry-import", options['db'], options['host'])
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
    with switch_db(dbmodels.OmimEntry, "cmd-omimentry-import") as OmimEntry:
        try:
            entry = OmimEntry.objects.get(mimNumber = record['mimNumber'])
            entry.update(**record)
        except OmimEntry.DoesNotExist:
            entry = OmimEntry(**record)
        except OmimEntry.MultipleObjectsReturned:
            raise Exception(u"有多条记录，需要人工核查!")
        except:
            raise Exception(u"在数据库查询时出现未知错误")
        entry.save()

def download(cmdobj, **opt):
    u"""
    通过mimNumber从http://api.omim.org/api/entry下载信息，并导入到数据库中omim_entry表中
    这种方法下载的内容和导入会有不同需要注意，例如clinicalSynopsis下的mimNumber, prefix, preferredTitle等待都不会下载
    """
    register_connection("cmd-download", opt['db'], opt['host'])
    OmimEntry = switch_db(dbmodels.OmimEntry, "cmd-download").cls
    # 确定需要更新的mimNumber
    if opt['mimNumber']:
        mims = opt['mimNumber']
    else:
        downlist = parser.ParseEntryDownload(opt['input'])
        mims = downlist.mims
    # 下载后导入数据库(根据clean有不同选择)
    http = urllib3.PoolManager()
    url = 'http://api.omim.org/api/entry'
    fields = {'apiKey': opt['apikey'], 'include': 'all', 'format': 'json'}
    for mim in mims:
        # 先下载，这样可以避免数据先清空
        print "Going through", mim
        fields['mimNumber'] = mim
        r = http.request('GET', url, fields = fields)
        if not r.status == 200:
            soup = BeautifulSoup(r.data,'lxml')
            print "Error for mimNumber", mim
            print "\t\t",soup.h1.string
            continue
        data = json.loads(r.data.decode('utf-8'))
        if not len(data['omim']['entryList']):
            print 'mimNumber', mim, "不存在"
            continue
        data = data['omim']['entryList'][0]['entry']
        clinicalSynopsis = data.get('clinicalSynopsis')
        if isinstance(clinicalSynopsis,dict):
            if clinicalSynopsis['oldFormatExists']:
                for key, value in clinicalSynopsis['oldFormat'].iteritems():
                    if isinstance(value, (str, unicode)):
                        clinicalSynopsis['oldFormat'][key] = re.sub("\s*\{.+?\}\s*","",value).replace("\n","")
            else:
                for key, value in clinicalSynopsis.iteritems():
                    if isinstance(value,(str, unicode)):
                        clinicalSynopsis[key] = re.sub("\s*\{.+?\}\s*","",value).replace("\n","")
        textSectionList = data.get('textSectionList')
        if isinstance(textSectionList,list):
            textSection = []
            for item in textSectionList:
                textSection.append(item.get("textSection"))
        entryDL = {}
        for key in 'titles clinicalSynopsisExists referenceList contributors creationDate prefix seeAlso status editHistory textSectionList clinicalSynopsis mimNumber'.split():
            if key == 'titles':
                entryDL['title'] = data.get(key)
            elif key == 'textSectionList':
                entryDL[key] = textSection
            elif key == 'mimNumber':
                entryDL[key] = mim
            elif key == 'creationDate':
                entryDL['createDate'] = data.get(key)
            else:
                entryDL[key] = data.get(key)
        # 导入数据库
        try:
            entry = OmimEntry.objects.get(mimNumber = mim)
            if opt['clean']:
                entry.delete()
                entry.save()
                entry = OmimEntry(**entryDL)
            else:
                if isinstance(entryDL['clinicalSynopsis'],dict):
                    set_clinicalSynopsis = {}
                    for key, value in entryDL['clinicalSynopsis'].iteritems():
                        entryDL['set__clinicalSynopsis__'+key] = entryDL['clinicalSynopsis'][key]
                entryDL.pop('clinicalSynopsis')
                entry.update(**entryDL)
        except OmimEntry.DoesNotExist:
            entry = OmimEntry(**entryDL)
        except OmimEntry.MultipleObjectsReturned:
            raise Exception(u"有多条记录，需要人工核查!")
        entry.save()



