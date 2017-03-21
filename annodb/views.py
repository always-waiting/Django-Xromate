# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
import models
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
    result = models.DgvVarient.objects(**query).limit(20)
    #logger.error(result)
    return JsonResponse(
        [ json.loads(item.to_json()) for item in result ],
        safe=False
    )
    #return HttpResponse(res)

def ucscrefgene(request):
    """
    按照坐标选取重合ucsc refgene区域,规则如下:
    """
    chrom = request.GET['chr']
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    query = {
        'chrom': chrom,
        'txStart__lte': end,
        'txEnd__gte': start,
    }
    result = models.UcscRefflat.objects(**query)
    return JsonResponse(
        [json.loads(item.to_json()) for item in result],
        safe=False
    )

def omimgenemap(request):
    """
    按照坐标选取重合OMIM GeneMap区域,规则如下:
    """
    chrom = request.GET['chr']
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    query = {
        'chromosomeSymbol': chrom,
        'chromosomeLocationStart__lte': end,
        'chromosomeLocationEnd__gte': start,
        'phenotypeMapList__ne': None,
    }
    result = models.OmimGenemap.objects(**query)
    #logger.info(result)
    return JsonResponse(
        [json.loads(item.to_json()) for item in result],
        safe = False
    )

def omimmorbidmap(request):
    """
    按照坐标选取重合OMIM Morbidmap区域,规则如下:
    """
    chrom = request.GET['chr']
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    query = {
        'chr': chrom,
        'start__lte': end,
        'end__gte': start,
        'phenotypeMappingKey__gt': 2,
    }
    result = models.OmimMorbidmap.objects(**query)
    return JsonResponse(
        [json.loads(item.to_json()) for item in result],
        safe = False
    )

def deciphercnv(request):
    """
    按照坐标选取重合Decipher CNV区域,规则如下:
    """
    chrom = request.GET['chr']
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    query = {
        'chr': chrom,
        'start__lte': end,
        'end__gte': start,
    }
    result = models.DecipherCnv.objects(**query)
    return JsonResponse(
        [json.loads(item.to_json()) for item in result],
        safe = False
    )

def clinvar(request):
    """
    按照坐标选取重合Clinvar区域,规则如下:
    """
    chrom = request.GET['chr']
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    query = {
        'chr': chrom,
        'start__lte': end,
        'end__gte': start
    }
    result = models.ClinVar.objects(**query)
    #logger.info(result)
    return JsonResponse(
        [json.loads(item.to_json()) for item in result],
        safe=False,
    )

def genereview(request):
    """
    按照坐标选取重合GeneReview区域,规则如下:
    """
    chrom = request.GET['chr']
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    query = {
        'chr': chrom,
        'start__lte': end,
        'end__gte': start
    }
    result = models.GeneReview.objects(**query)
    #logger.info(result)
    return JsonResponse(
        [json.loads(item.to_json()) for item in result],
        safe=False,
    )

def deciphersyndrome(request):
    """
    按照坐标选取重合Decipher Syndrome区域,规则如下:
    """
    chrom = request.GET['chr']
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    query = {
        'chr': chrom,
        'start__lte': end,
        'end__gte': start
    }
    result = models.DecipherSyndrome.objects(**query)
    #logger.info(result)
    return JsonResponse(
        [json.loads(item.to_json()) for item in result],
        safe=False,
    )
