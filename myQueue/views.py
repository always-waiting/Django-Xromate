# coding: utf-8
from django.shortcuts import render
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from Queue import Queue
# Create your views here.

logger = logging.getLogger('django')
q = Queue()

def index(request):
    return render(request, 'myQueue/home.html')

@csrf_exempt
#@ensure_csrf_cookie
def fid_get(request):
    if request.method == 'GET':
        return render(request, 'myQueue/fid.html')
    elif request.method == 'POST':
        fid = request.POST['fid']
        q.put(fid)
        #logger.info(q.qsize())
        return render(request, 'myQueue/fid.html')

def fid_delete(request):
    if q.empty():
        return HttpResponse("空")
    else:
        getitem = q.get()
        q.task_done()
        return HttpResponse(getitem)
