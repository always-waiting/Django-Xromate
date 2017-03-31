from __future__ import unicode_literals

from django.apps import AppConfig
from mysite.settings import DATABASES
import re

class XromateConfig(AppConfig):
    name = DATABASES['xromate']['NAME']
    db = DATABASES['xromate']['NAME']
    host = DATABASES['xromate']['HOST']
    alias = DATABASES['xromate']['alias']


def dumpstring(obj, newline="\n", space="\t", level=0):
    string = []
    if type(obj) == dict:
        string.append("%s{%s" % (level*space, newline))
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                string.append(u"%s%s =>%s" % ((level+1)*space, k, newline))
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
                string.append(u"%s%s%s" % ((level+1)*space, v, newline))
        string.append("%s]%s" % (level*space, newline))
    else:
        if isinstance(obj, str):
            strobj = obj
        elif isinstance(obj, unicode):
            strobj = obj.encode("utf8")
        else:
            try:
                strobj = str(obj)
            except Exception,e:
                strobj = "Unknown"
        addlevelobj = re.sub("\n","\n"+level*space, strobj)
        string.append(u"%s%s%s" % (level*space, addlevelobj.decode("utf8"), newline))
    try:
        return "".join(string).encode("utf8")
    except Exception:
        return "".join(string)



