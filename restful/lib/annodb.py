# coding: utf-8
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

# Create api/annodb views here
def dgv(request):
    chrnum = request.GET['chr']
    start = request.GET['start']
    end = request.GET['end']
    redirect_url = reverse("annodb_dgv")
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
