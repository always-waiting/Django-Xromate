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
    """
    按照坐标选取重合dgv变异.有如下规则:
        1. dgv.start <= end
        2. dgv.end >= start
        3. dgv.mergedOrSample = S
        4. dgv.chr = chr
        5. limit = 20
    在前端展示时,也有规则，具体规则见前段相应代码
    """
    chrnum = request.GET['chr']
    chrnum = int(chrnum) if chrnum.isdigit() else chrnum
    start = request.GET['start']
    start = int(start)
    end = request.GET['end']
    end = int(end)
    query = {
        'chr': chrnum,
        'start__lte': end,
        'end__gte': start,
        'mergedOrSample': 'S',
    }
    result = DgvVarient.objects(**query).limit(20)
    #logger.error(result)
    return JsonResponse(
        [ json.loads(item.to_json()) for item in result ],
        safe=False
    )
    #return HttpResponse(res)
