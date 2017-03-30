# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from mysite.decorator import login_required
from models import Flowcells, Samples, search_samples
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import datetime

logger = logging.getLogger('django')

# Create your views here.

def study_index(request):
    return render(request, 'Xromate/study_index.html')

@login_required(login_url='login/')
def index(request):
    return render(request, 'Xromate/index.html')

def projects(request, project='CNV'):
    if project == 'MCC':
        headers = ["Flowcell",u'导入时间', u'总样本数',u'待分析',u'已同步']
    else:
        headers = ['Flowcell', u'导入时间', u'总样本数', u'待分析', u'已提交', u'审核完毕', u'已同步', u'已驳回']
    flowcells = Flowcells.objects(project=project).order_by("-id")
    paginator = Paginator(flowcells, 25)
    page = request.GET.get('page')
    if page:
        if page == '0': page = 1
        if int(page) > paginator.num_pages: page = paginator.num_pages
    #logger.info("page is: %s" % page)
    pageinfo = {'total': paginator.num_pages}
    try:
        flowcells_show = paginator.page(page)
        pageinfo['current'] = int(page)
    except PageNotAnInteger:
        flowcells_show = paginator.page(1)
        pageinfo['current'] = 1
    except EmptyPage:
        flowcells_show = paginator.page(paginator.num_pages)
        pageinfo['current'] = int(paginator.num_pages)

    if pageinfo['current'] - 9 < 0:
        pageinfo['range'] = list(range(1, min(10,pageinfo['total']+1)))
    elif pageinfo['current'] + 9 > pageinfo['total']:
        pageinfo['range'] = list(range(max(pageinfo['total']-9,1), pageinfo['total']+1))
    else:
        pageinfo['range'] = list(range(pageinfo['current']-4,pageinfo['current']+5))
    return render(
        request,
        'Xromate/projects.html',
        {
            'test': '这是一个测试',
            'project': project,
            'headers': headers,
            'flowcells': flowcells_show,
            'pageinfo' : pageinfo,
        }
    )

def samples_count(request, project, flowcell):
    query = {'flowcell': flowcell, 'project': project}
    print request.GET
    for k, v in request.GET.iteritems():
        query[k] = v
    queryset = search_samples(**query)
    return JsonResponse({'number': queryset.count(),'time':'abc'})

