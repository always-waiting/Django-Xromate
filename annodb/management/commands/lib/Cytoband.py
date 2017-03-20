# encoding: utf-8

import annodb.models as dbmodels
import annodb.lib.parser as parser
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
import re

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

def update_omimmorbidmap(cmdobj, **opt):
    """
    通过输入的cytoband region，从cytoband中查询后把坐标信息更新到omim morbidmap表
    默认为更新omim morbidmap表中所有的cytoband region
    """
    register_connection("cytoband", opt['cytodb'], opt['cytohost'])
    register_connection("morbid", opt['morbiddb'], opt['morbidhost'])
    # 定位要确定坐标的cytoband区域
    cytolist = []
    if opt['cytoband']:
        cytolist.extend(opt['cytoband'])
    else:
        with switch_db(dbmodels.OmimMorbidmap, "morbid") as OmimMorbidmap:
            for cyto in OmimMorbidmap.objects.only('cytoLocation'):
                cytolist.append(cyto.cytoLocation)
    if opt['debug']: print "cytoband total: %s" % len(cytolist)
    for cyto in cytolist:
        # 通过Cytoband表确定坐标
        if opt['debug']: print '从cytoband确定%s区域的坐标' % cyto
        with switch_db(dbmodels.Cytoband, "cytoband") as Cytoband:
            coor = Cytoband.cytoband_region_to_coordinates(cyto)
        if not coor:
            if opt['debug']: print "%s has not coor next" % cyto
            continue
        # 通过cyto region确定需要更新的morbid
        if opt['debug']: print "更新%s的坐标到omim morbidmap" % cyto
        with switch_db(dbmodels.OmimMorbidmap, "morbid") as OmimMorbidmap:
            morbids = OmimMorbidmap.objects(cytoLocation=cyto)
            for morbid in morbids:
                morbid.update(**coor)
                morbid.save()

