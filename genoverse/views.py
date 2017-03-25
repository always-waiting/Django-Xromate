#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging
from mysite.decorator import login_required

logger = logging.getLogger('django')
#from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login/")
def index(request):
    #return HttpResponse(u"测试genoverse的主页!")
    return render(request, 'genoverse/home.html');

def embed(request):
    return render(request, 'genoverse/embed.html');

def add_tracker(request):
    return render(request, 'genoverse/add_tracker.html');
