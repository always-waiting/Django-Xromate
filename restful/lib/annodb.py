# coding: utf-8
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger('django')


# Create api/annodb views here
def dgv(request):
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_dgv")
    if request.GET.has_key('type'):
        cnvtype = request.GET['type']
        #logger.info(cnvtype)
        redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s&type=%s" % (chrnum, start, end, cnvtype)])
    else:
        redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def ucscrefgene(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_ucscrefgene")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def omimgenemap(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_omimgenemap")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def omimmorbidmap(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_omimmorbidmap")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def deciphercnv(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_deciphercnv")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def clinvar(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_clinvar")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def genereview(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_genereview")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def deciphersyndrome(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_deciphersyndrome")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)

def pubmed(request):
    """
    通过参数获得数据库中的区段信息
    """
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_pubmed")
    redirect_url = "?".join([redirect_url, "chr=%s&start=%s&end=%s" % (chrnum, start, end)])
    return redirect(redirect_url)
