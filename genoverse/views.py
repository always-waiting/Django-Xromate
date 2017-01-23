#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse(u"测试genoverse的主页!")
    return render(request, 'genoverse/home.html');

def embed(request):
    return render(request, 'genoverse/embed.html');

def add_tracker(request):
    return render(request, 'genoverse/add_tracker.html');

