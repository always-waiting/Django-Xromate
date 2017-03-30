from __future__ import unicode_literals

from django.db import models
import mongoengine as mongoe
from lib.User import User
from lib.Flowcell import Flowcells
from lib.Sample import Samples
from apps import XromateConfig
# Create your models here.

mongoe.connect(
    XromateConfig.db,
    host=XromateConfig.host,
    alias=XromateConfig.alias
)

def search_samples(**opt):
    rawquery = {}
    query = {}
    fquery = {}
    if opt.has_key('flowcell'):
        fquery['name'] = opt['flowcell']
        del opt['flowcell']
    if opt.has_key('project'):
        fquery['project'] = opt['project']
        del opt['project']
    if fquery.keys():
        flowcell = Flowcells.objects(__raw__=fquery)[0]
        rawquery['flowcell.$id'] = flowcell.id
    #print opt
    for k,v in opt.iteritems():
        if k.find('__') != -1:
            query[k] = eval(v)
        else:
            rawquery[k] = v
    print query
    return Samples.objects(__raw__=rawquery, **query)



