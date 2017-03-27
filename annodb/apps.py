from __future__ import unicode_literals

from django.apps import AppConfig
from mysite.settings import DATABASES
import re

class AnnodbConfig(AppConfig):
    name = DATABASES['annodb']['NAME']
    db = DATABASES['annodb']['NAME']
    host = DATABASES['annodb']['HOST']
    alias = DATABASES['annodb']['alias']


def dumpstring(obj, newline="\n", space="\t", level=0):
    string = []
    if type(obj) == dict:
        string.append("%s{%s" % (level*space, newline))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                string.append("%s%s =>%s" % ((level+1)*space, k, newline))
                string.append(dumpstring(v, level = level+1))
            else:
                string.append("%s%s => %s%s" % ((level+1)*space, k, v, newline))
        string.append("%s}%s" % (level*space, newline))
    elif type(obj) == list:
        string.append("%s[%s" % (level*space, newline))
        for v in obj:
            if hasattr(v, '__iter__'):
                string.append(dumpstring(v, level = level+1))
            else:
                string.append("%s%s%s" % ((level+1)*space, v, newline))
        string.append("%s]%s" % (level*space, newline))
    else:
        strobj = str(obj)
        addlevelobj = re.sub("\n","\n"+level*space, strobj)
        string.append("%s%s%s" % (level*space, addlevelobj, newline))
    return "".join(string)



