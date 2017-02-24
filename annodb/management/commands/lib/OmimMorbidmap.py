# encoding: utf-8
import os
import re
import annodb.models as dbmodels
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
from contextlib import nested
import json

def omim_morbidmap_import(cmdobj, **options):
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
            # 解析一行
            record = parser_morbidmap(chunk)
            #　导入
            import_omim_morbidmap(record)

def import_omim_morbidmap(record):
    with switch_db(dbmodels.OmimMorbidmap, "cmd-import") as OmimMorbidmap:
        try:
            item = OmimMorbidmap(**record)
            item.save()
        except Exception, e:
            print e
            print record

def parser_morbidmap(chunk):
    items = chunk.split("\t")
    phenotype = {}
    try:
        phenotype_desc = items[0]
        phenotype['geneSymbols'] = items[1]
        phenotype['mimNumber'] = int(items[2])
        phenotype['cytoLocation'] = items[3]
        if re.match("(.*)\,\s(\d{6})\s?\((\d+)\)", phenotype_desc):
            get = re.match("(.*)\,\s(\d{6})\s?\((\d+)\)", phenotype_desc)
            phenotype['phenotype'] = get.group(1)
            phenotype['phenotypeMimNumber'] = int(get.group(2))
            phenotype['phenotypeMappingKey'] = int(get.group(3))
        elif re.match("(.*)\,\s(\d{6})", phenotype_desc):
            get = re.match("(.*)\,\s(\d{6})", phenotype_desc)
            phenotype['phenotype'] = get.group(1)
            phenotype['phenotypeMimNumber'] = int(get.group(2))
        elif re.match("(.*)\s?\((\d+)\)", phenotype_desc):
            get = re.match("(.*)\s?\((\d+)\)", phenotype_desc)
            phenotype['phenotype'] = get.group(1)
            phenotype['phenotypeMimNumber'] = phenotype['mimNumber']
            phenotype['phenotypeMappingKey'] = int(get.group(2))
        else:
            phenotype['phenotype'] = phenotype_desc
            phenotype['phenotypeMimNumber'] = phenotype['mimNumber']
    except Exception, e:
        print e
        print "出现错误"
        print chunk
    return phenotype


