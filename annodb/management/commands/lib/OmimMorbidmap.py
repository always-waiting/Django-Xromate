# encoding: utf-8
import os
import re
import annodb.models as dbmodels
from mongoengine import register_connection
import annodb.lib.parser as parser
from mongoengine.context_managers import switch_db
from contextlib import nested
import json

def update_entry(cmdobj, **opt):
    """
    通过mimNumber从morbidmap中获取信息更新到entry中
    $entry->set("/geneMap/phenotypeMapList", $phenomaps{$mim});
    这个perl命令不知道是什么
    """
    register_connection("cmd-update-sub", opt['morbidmapdb'], opt['morbidmaphost'])
    register_connection("cmd-update-obj", opt['entrydb'], opt['entryhost'])
    with switch_db(dbmodels.OmimEntry, "cmd-update-obj") as OmimEntry:
        with switch_db(dbmodels.OmimMorbidmap,"cmd-update-sub") as OmimMorbidmap:
            if opt['mimNumber']:
                mimsets = set(opt['mimNumber'])
            else:
                a = OmimMorbidmap.objects.only("mimNumber")
                mimsets = set([item.mimNumber for item in a])
            for mim in mimsets:
                morbidmap_list = OmimMorbidmap.objects(mimNumber = mim)
                phenomaps_list = json.loads(morbidmap_list.to_json())
                map(lambda x: x.pop('_id'), phenomaps_list)
                map(lambda x: x.pop('geneMapExists',""), phenomaps_list)
                phenomaps = []
                map(lambda x: phenomaps.append({'phenotypeMap': x}), phenomaps_list)
                try:
                    entry = OmimEntry.objects.get(mimNumber = mim)
                    entry.update(phenotypeMapExists = True, phenotypeMapList = phenomaps)
                    entry.save()
                except OmimEntry.DoesNotExist:
                    print mim, "不在entry表中"
                """
                $entry->set("/geneMap/phenotypeMapList", $phenomaps{$mim});
                不知道用来做什么的
                """

def update_genemap(cmdobj, **opt):
    """
    通过mimNumber从morbidmap中获取信息更新到genemap中
    并修改morbidmap的geneMapExists字段。如果没有mimNumber则处理全部
    """
    try:
        register_connection("cmd-update-sub", opt['morbidmapdb'], opt['morbidmaphost'])
        register_connection("cmd-update-obj", opt['genemapdb'], opt['genemaphost'])
    except:
        raise Exception("链接数据库失败")
    with switch_db(dbmodels.OmimGenemap, "cmd-update-obj") as OmimGenemap:
        with switch_db(dbmodels.OmimMorbidmap,"cmd-update-sub") as OmimMorbidmap:
            if opt['mimNumber']:
                mimsets = set(opt['mimNumber'])
            else: # 从数据库morbidmap表获得所有mimNumber
                a = OmimMorbidmap.objects.only("mimNumber")
                mimsets = set([item.mimNumber for item in a])
            # 处理所有mimNumber
            for mim in mimsets:
                try:
                    genemap = OmimGenemap.objects.get(mimNumber = mim)
                    morbidmap_list = OmimMorbidmap.objects(mimNumber = mim)
                    phenomaps_list = json.loads(morbidmap_list.to_json())
                    map(lambda x: x.pop('_id'), phenomaps_list)
                    map(lambda x: x.pop('geneMapExists',""), phenomaps_list)
                    phenomaps = []
                    map(lambda x: phenomaps.append({'phenotypeMap': x}), phenomaps_list)
                    genemap.update(phenotypeMapList = phenomaps)
                    genemap.save()
                    map(lambda x: x.update(geneMapExists = True), morbidmap_list)
                except Exception, e:
                    print e




def importdb(cmdobj, **options):
    """
    导入morbidmap.txt到数据库
    """
    if not os.path.exists(options['input']):
        raise Exception(options['input'] + " not exists")
    try:
        register_connection('cmd-import', options['db'], options['host'])
        # 删除数据库中原有记录
        with switch_db(dbmodels.OmimMorbidmap, "cmd-import") as OmimMorbidmap:
            OmimMorbidmap.objects.delete()
    except:
        raise Exception(options['host']+'/'+options['db']+"链接失败")
    with open(options['input']) as f:
        for chunk in f:
            chunk = chunk.lstrip().rstrip()
            if chunk.startswith("#"): continue
            if not chunk: continue
            morbidmapone = parser.ParseMorbidmap(chunk)
            import_one(morbidmapone.record)

def import_one(record):
    with switch_db(dbmodels.OmimMorbidmap, "cmd-import") as OmimMorbidmap:
        try:
            item = OmimMorbidmap(**record)
            item.save()
        except Exception, e:
            print e
            print record

