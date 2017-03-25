# encoding: utf-8
from django.shortcuts import render
import logging
import urllib
import urllib2
import json
from django.http import HttpResponseRedirect,HttpResponse
from mysite import settings
from django.core.urlresolvers import reverse
import logging

logger = logging.getLogger('django')

# Create your views here.
GITHUB_CLIENTID = settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = settings.GITHUB_CALLBACK
GITHUB_AUTHORIZE_URL = settings.GITHUB_AUTHORIZE_URL

def login(request):
    return render(request, 'login/login.html')

def _get_refer_url(request):
    refer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if refer_url.startswith('http') and host in refer_url:
        refer_url = '/'
    if 'back_url' in request.session:
        refer_url = request.session['back_url']
        del request.session['back_url']
    return refer_url


def github_login(request):
    data = {
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'redirect_uri': GITHUB_CALLBACK,
        'state': _get_refer_url(request),
    }
    github_auth_url = '%s?%s' % (
        GITHUB_AUTHORIZE_URL, urllib.urlencode(data)
    )
    #print ('git_hub_auth_url',github_auth_url)
    return HttpResponseRedirect(github_auth_url)

def github_auth(request):
    template_html = 'login/login.html'
    if 'code' not in request.GET:
        return render(request, template_html)

    code = request.GET.get('code')
    # 确定back_url
    back_path = request.GET.get('state')
    # 获得acccess_token
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'client_id': GITHUB_CLIENTID,
        'client_secret': GITHUB_CLIENTSECRET,
        'code': code,
        'redirect_uri': GITHUB_CALLBACK,
    }
    data = urllib.urlencode(data)
    binary_data = data.encode('utf-8')
    headers = {'Accept': 'application/json'}
    req = urllib2.Request(url, binary_data, headers)
    response = urllib2.urlopen(req)
    result = json.loads(response.read())
    access_token = result['access_token']
    # 获得用户名
    url = 'https://api.github.com/user?access_token=%s' % (access_token)
    response = urllib2.urlopen(url)
    data = json.loads(response.read().decode('ascii'))
    request.session['username'] = data['name']
    request.session['is_authenticated'] = True
    # 通过back_path确定需要处理的数据库
    if back_path.startswith('/xromate'):
        '''
        向Xromate数据库查询用户，如果没有，添加用户．如果存在，目前什么也不做
        '''
        pass
    elif back_path.startswith('/monitor'):
        '''
        向Monitor数据库查询用户，如果没有，添加用户．如果存在，目前什么也不做
        '''
        pass
    else:
        pass
    # 返回原先的访问地址
    return HttpResponseRedirect(back_path)

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    request.session['is_authenticated'] = False
    return HttpResponseRedirect(reverse('web_login'))

