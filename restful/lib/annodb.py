# coding: utf-8
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger('django')


# Create api/annodb views here
def table_locs(request, table, locs):
    if request.method == 'GET':
        redirect_url = reverse("annodb_table_locs", kwargs={'table':table, 'locs':locs})
        query = []
        for get in request.GET:
            query.append("=".join([get,request.GET[get]]))
            #logger.info(get)
        if query:
            querystr = "&".join(query)
            redirect_url = "?".join([redirect_url, querystr])
        return redirect(redirect_url)
