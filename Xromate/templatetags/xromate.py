# encoding: utf-8
from django import template
from django.template.defaultfilters import stringfilter
import pytz
import datetime
import re
import json
from bson import json_util
register = template.Library()
tz = pytz.timezone('Asia/Shanghai')

#@register.filter(name='cut')

@register.filter
def to_json(data):
    return json_util.dumps(data)


@register.filter
def get_item(data, key):
    if type(data) == dict:
        return data.get(key, '')
    if type(data) == list:
        try:
            return data[int(key)]
        except Exception,e:
            return ""

@register.filter
@stringfilter
def fupper(value):
    if value:
        return value[0].upper()
    else:
        return ''

@register.filter
def parse_sickphenop(value, sampledoc):
    code2des = [u'空', u'智力障碍', u'特殊面容', u'先天性心脏病', u'发育迟缓', u'肌无力', u'肢体畸形', u'脏器畸形', u'自闭症', u'生殖系统畸形', u'其他']
    codes = value.replace(",",";").split(";")
    code2des[10] = "%s: %s" % (code2des[10], sampledoc.remote.othersickphenop)
    result = ['<div class="ui bulleted list">']
    for i in codes:
        if i.isdigit():
            i = int(i)
            result.append("<div class='item'>%s</div>" % code2des[i])
    result.append("</div>")
    try:
        return "".join(result)
    except Exception, e:
        return u"出现错误联系开发"


@register.filter
def parse_ultrasound(value, sampledoc):
    sound = [u'未见异常',u'胎儿结构异常',u'软指标高风险',u'介入性手术治疗',u'其他']
    result = []
    for i in value.replace(";",",").split(','):
        if i.isdigit() and int(i) in [1,2,3,4,5]:
            i = int(i)
            result.extend([str(i),'.',sound[i-1],":"])
            ultrasoundtext_index = "ultrasoundtext" if i == 1 else "ultrasoundtext%d" % (i-1)
            ultrasoundtext_content = getattr(sampledoc.remote,ultrasoundtext_index)
            if ultrasoundtext_content:result.append("%s\n" % ultrasoundtext_content)
        else:
            if value: result.append(u"远程sound字段内容为: %s" % value)
    try:
        return "".join(result)
    except Exception,e:
        return u"出现错误联系开发"



@register.filter
def time_local(value):
    if isinstance(value, datetime.datetime):
        try:
            loc_dt = pytz.utc.localize(value).astimezone(tz)
            return loc_dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return value.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return ""

@register.simple_tag(takes_context=True)
def reject_list(context):
    if not ('sample_rejects' in context and 'cnv_rejects' in context): return ''
    sample_rejects = context['sample_rejects']
    cnv_rejects = context['cnv_rejects']
    pre = 0
    current = 0
    result = []
    for log in sample_rejects:
        result.append(u'<tr>')
        current = log.time
        cnv_get = filter(lambda x: x.time>pre and x.time<current, cnv_rejects)
        rows_count = len(cnv_get) + 1
        reject_time = pytz.utc.localize(datetime.datetime.fromtimestamp(log.time))
        result.append(u"<td rowspan=%s>%s</td>" % (rows_count, reject_time.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")))
        result.append(u"<td class='center aligned'><h5>CNV位置</h5></td>")
        result.append(u"<td class='center aligned'><h5>CNV驳回原因</h5></td>")
        result.append(u"<td rowspan=%s>%s</td>" % (rows_count, log.comment))
        result.append(u"<td rowspan=%s>%s</td>" % (rows_count, log.user))
        result.append(u"</tr>")
        for cnv in cnv_get:
            result.append("<tr><td>%s</td><td>%s</td></tr>" % (cnv.location, cnv.comment))
        pre = current
    return ''.join(result)

@register.simple_tag(takes_context=True)
def body_data_generation(context):
    relist = []
    if 'username' in context:
        relist.append("data-username=%s" % context['username'])
    if 'project' in context and context['project']:
        relist.append("data-project=%s" % context['project'])
    if 'flowcell' in context and context['flowcell']:
        relist.append("data-flowcell=%s" % context['flowcell'])
    if 'sample' in context and context['sample']:
        relist.append("data-sample=%s" % context['sample'])
    return ' '.join(relist)

@register.assignment_tag
def to_list(*args):
    return list(args)

@register.assignment_tag
def to_dict(**kargs):
    return kargs
