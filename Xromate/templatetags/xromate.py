from django import template
from django.template.defaultfilters import stringfilter
import pytz
import datetime
register = template.Library()

#@register.filter(name='cut')
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
@stringfilter
def fupper(value):
    if value:
        return value[0].upper()
    else:
        return ''
@register.filter
def time_local(value):
    tz = pytz.timezone('Asia/Shanghai')
    utc = pytz.utc
    if isinstance(value, datetime.datetime):
        try:
            utc_dt = utc.localize(value)
            loc_dt = utc_dt.astimezone(tz)
            return loc_dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return value.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return ""


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

