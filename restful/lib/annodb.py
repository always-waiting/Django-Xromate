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
