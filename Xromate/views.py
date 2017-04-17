# encoding: utf-8
import os
import re
from django.shortcuts import render
from Xromate.apps import XromateConfig
from django.http import HttpResponse, JsonResponse
from mysite.decorator import login_required
from models import Flowcells, Samples, search_samples, search_mccs, search_cnvs, Users
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import logging
import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.urlresolvers import reverse

logger = logging.getLogger('django')
chromlist = ['X', 'Y']
chromlist.extend(range(1,23))

# Create your views here.

def study_index(request):
    return render(request, 'Xromate/study_index.html')

@login_required(login_url='login/')
def index(request):
    return render(request, 'Xromate/index.html')

def projects_retrieve(request, project='CNV'):
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
            'headers': headers,
            'flowcells': flowcells_show,
            'pageinfo' : pageinfo,
        }
    )

def samples_count(request, project, flowcell):
    query = {'flowcell': flowcell, 'project': project}
    for k, v in request.GET.iteritems():
        query[k] = v
    if project == 'MCC':
        queryset = search_mccs(**query)
    else:
        queryset = search_samples(**query)
    #return HttpResponse(queryset.count())
    return JsonResponse({'number': queryset.count(),'time':'abc'})

def projects_flowcells_retrieve(request, project, flowcell):
    process2zhcn = {
        'unanalyzed'    : '未分析',
        'analyzed'      : '已分析',
        'rejected'      : '已驳回',
        'confirmed'     : '已审核',
        'synchronized'  : '已同步',
        'unsubmitted'   : '未分析',
        'submitted'     : '已提交',
    }
    process2class = {
        'unsubmitted'   : 'negative',
        'submitted'     : 'warning',
        'confirmed'     : 'positive',
        'rejected'      : 'negative',
        'synchronized'  : 'positive',
    }
    if project == 'MCC':
        headers = ['样品编号','预测结果','结论','状态','提交时间','分析人']
        queryset = search_mccs(flowcell=flowcell, project = project)
        queryset = queryset.order_by('prediction')
    else:
        headers = ['样品编号', '性别', '总计', '提交', '确认', '状态', '结论', '报告日期', '简述', '分析人', '审核人']
        queryset = search_samples(flowcell=flowcell, project=project)
        queryset = queryset.order_by('name')

    return render(
        request,
        'Xromate/projects_flowcells_retrieve.html',
        {
            'process2class': process2class,
            'process2zhcn': process2zhcn,
            'headers': headers,
            'samples': queryset,
        }
    )

def sample_cnvs_count(request, project, flowcell, sample):
    query = {'project': project, 'flowcell': flowcell, 'sample': sample}
    for k, v in request.GET.iteritems():
        query[k] = v
    queryset = search_cnvs(**query)
    return HttpResponse(queryset.count())
    #JsonResponse({'number': queryset.count()})

def profile(request):
    fieldstr = request.GET.get('fields')
    if fieldstr:
        fields = fieldstr.split(",")
        try:
            user = Users.objects.get(username = request.session['username'])
        except KeyError,e:
            return JsonResponse({'error': "KeyError: %s" % e})
        except Exception,e:
            return JsonResponse({'error': "Unknown Error: %s" % e})
        retjson = { field: getattr(user, field) for field in fields if hasattr(user, field)}
        return JsonResponse(retjson)
    else:
        return JsonResponse({'error': "not fields to search"})


def users_retrieve(request):
    return JsonResponse(json.loads(Users.objects().to_json()), safe=False)

@csrf_exempt
@api_view(['PATCH', 'GET'])
def projects_flowcells_samples_retrieve(request, project, flowcell, sample):
    if request.method == 'PATCH':
        query = {}
        if request.data.get('analyst'): query['analyst'] = request.data['analyst']
        if request.data.get('auditor'): query['auditor'] = request.data['auditor']
        if not hasattr(query, 'process'):
            #logger.info("没有process属性，直接更新数据库")
            sample = search_samples(flowcell=flowcell, project=project, name=sample)
            sample.update(**query)
        else:
            logger.info("有process属性，分析阶段的问题")
        return Response(query)
    if request.method == 'GET':
        sample = search_samples(flowcell=flowcell, project=project, name=sample)
        sampledoc = sample.first()
        summary = sampledoc.summary or {}
        baseinfo = {
            "No.": sampledoc.name, 'Case ID': sampledoc.remote.caseid, 'Gender': sampledoc.gender or 'unknown',
            'Total Reads': format(summary.get('total_reads',0),",d"), 'Unique Reads': format(summary.get('unique_reads',0),",d"),
            'PCR Duplication': format(summary.get('pcr_duplication', 0),",d"), 'Unique Percentage': '%.2f%%' % summary.get('unique_percent', 0),
            'Unique GC Content': '%.2f%%' % summary.get('unique_gc',0), 'Redundancy': '%.2f%%' % summary.get('redundancy',0),
            'NIPT Comment': summary.get('nipt_comment',''), 'MCC Result': sampledoc.remote.mcc
        }
        remoteinfo = json.loads(sampledoc.remote.to_json())
        sample_rejects = sampledoc.search_logs(operation='reject')
        cnv_rejects = []
        map(lambda x: cnv_rejects.extend(x.search_logs()), sampledoc.search_cnvs())
        return render(
            request,
            'Xromate/project_flowcell_sample_retrieve.html',
            {
                'chromlist': chromlist,
                'sampledoc': sampledoc,
                'baseinfo': baseinfo,
                'remoteinfo': remoteinfo,
                'sample_rejects': sample_rejects,
                'cnv_rejects': cnv_rejects,
            }
        )

@csrf_exempt
@api_view(['PUT'])
def project_flowcell_sample_remote_retrieve(request, project, flowcell, sample):
    if request.method == 'PUT':
        sample = search_samples(flowcell=flowcell, project=project, name=sample)
        sampledoc = sample.first()
        sampledoc.remote.pull()
        return Response(json.loads(sampledoc.remote.to_json()))

def project_flowcell_sample_chromosomes_list(request, project, flowcell, sample):
    sampledoc = search_samples(flowcell=flowcell, project=project, name=sample).first()
    cnvs = sampledoc.search_cnvs()
    chr2cnvs = cnvs.aggregate({'$group':{'_id':"$chr",'chrom':{'$push': "$$ROOT"}}})
    output = []
    for chrom in chromlist:
        output.append({
            'image': reverse('xromate_project_flowcell_sample_chromosome_retrieve', kwargs={'project':project, 'flowcell': flowcell, 'sample': sample, 'chrom': chrom}),
            'chrom': chrom,
        })
    for cnvlist in chr2cnvs:
        chrom = int(cnvlist['_id']) if cnvlist['_id'].isdigit() else cnvlist['_id']
        index = chromlist.index(chrom)
        output[index]['mosaic'] = filter(lambda x: x['type'] == 'Mosaic', cnvlist['chrom'])
        output[index]['cnvs'] = sorted(filter(lambda x: x['type'] == 'CNV', cnvlist['chrom']), key=lambda x: x['start'])
    return render(
        request,
        'Xromate/project_flowcell_sample_chromsomes_list.html',
        {
            'chromlist': chromlist,
            'sampledoc': sampledoc,
            'output': output,
        }
    )
    #return HttpResponse("开发图片展示页面")

#@api_view(['GET'])
def project_flowcell_sample_chromosome_retrieve(request, project, flowcell, sample, chrom, format=None):
    #logger.info(format)
    #logger.info(chrom)
    #return HttpResponse("开发获得图片url")
    filedir = "%s/%s/%s/SAMPLE-PNG/" % (XromateConfig.png_dir, project, flowcell)
    try:
        files = os.listdir(filedir)
    except Exception,e:
        logger.info(filedir)
        return HttpResponse(u"项目%s -> 批次%s ->PNG_WEB目录不存在" % (project,flowcell))
    for f in files:
        if re.match("%s.*chr%s.png" % (sample,chrom), f):
            filepath = "%s/%s" % (filedir, f)
    logger.info(filepath)
    try:
        data = open(filepath).read()
        return HttpResponse(data,content_type="image/jpeg")
    except Exception,e:
        return HttpResponse("Error")
