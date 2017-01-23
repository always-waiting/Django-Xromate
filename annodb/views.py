# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import DgvVarient
from django.http import JsonResponse
import logging
import json

logger = logging.getLogger('django')


# Create your views here.
def index(request):
    return render(request, 'annodb/home.html');

def dgv(request):
    chrnum = request.GET['chr']
    chrnum = int(chrnum) if chrnum.isdigit() else chrnum
    start = request.GET['start']
    start = int(start)
    end = request.GET['end']
    end = int(end)
    res = u"%s:%s--->%s在这里定义提出数据库DGV数据的方法" % (chrnum, start, end)
    #res = u"在这里定义提出数据库DGV数据的方法"
    query = {
        'chr': chrnum,
        'start__lte': end,
        'end__gte': start,
        'mergedOrSample': 'S',
    }
    result = DgvVarient.objects(**query).limit(20)
    #result = DgvVarient.objects(chr=10,start__lte=200000,end__gte=2000,mergedOrSample='S')
    logger.error(result)
    return JsonResponse(
        [ json.loads(item.to_json()) for item in result ],
        safe=False
    )
    #return HttpResponse(res)
