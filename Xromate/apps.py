from __future__ import unicode_literals

from django.apps import AppConfig
from mysite.settings import DATABASES
try:
    from mysite.settings import PNG_WEB_DIR
    png_dir_flag = 1
except Exception,e:
    print "You shold defined PNG_WEB_DIR in your settings files"
    png_dir_flag = 0
import re

class XromateConfig(AppConfig):
    name = DATABASES['xromate']['NAME']
    db = DATABASES['xromate']['NAME']
    host = DATABASES['xromate']['HOST']
    alias = DATABASES['xromate']['alias']
    remote_get_url = 'http://192.168.21.224/berry/Jrest/cnvService/getBerrygenomics'
    remote_put_url = 'http://192.168.21.224/berry/Jrest/cnvService/addBerrygenomics'
    png_dir = PNG_WEB_DIR if png_dir_flag else "/data/PNG_WEB"

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



