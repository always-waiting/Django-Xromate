# encoding: utf-8
from django.shortcuts import render
from mysite.decorator import login_required
import logging

logger = logging.getLogger('django')

# Create your views here.

def study_index(request):
    return render(request, 'Xromate/study_index.html')

@login_required(login_url='login/')
def index(request):
    return render(request, 'Xromate/index.html')

def projects(request, project='CNV'):
    if project == 'MCC':
        headers = ["Flowcell",u'导入时间', u'总样本数',u'待分析',u'已同步']
    else:
        headers = ['Flowcell', u'导入时间', u'总样本数', u'待分析', u'已提交', u'审核完毕', u'已同步', u'已驳回']
    return render(
        request,
        'Xromate/projects.html',
        {
            'test': '这是一个测试',
            'project': project,
            'headers': headers,
        }
    )
