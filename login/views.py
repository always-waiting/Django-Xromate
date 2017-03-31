# encoding: utf-8
from django.shortcuts import render
import logging
import urllib
import urllib2
import json
from django.http import HttpResponseRedirect,HttpResponse
from mysite import settings
from django.core.urlresolvers import reverse
from Xromate.lib.User import Users
import logging

logger = logging.getLogger('django')

# Create your views here.
# GITHUB
GITHUB_CLIENTID = settings.GITHUB_CLIENTID
GITHUB_CLIENTSECRET = settings.GITHUB_CLIENTSECRET
GITHUB_CALLBACK = settings.GITHUB_CALLBACK
GITHUB_AUTHORIZE_URL = settings.GITHUB_AUTHORIZE_URL
# GITLAB
GITLAB_CLIENTID = settings.GITLAB_CLIENTID
GITLAB_CLIENTSECRET = settings.GITLAB_CLIENTSECRET
GITLAB_CALLBACK = settings.GITLAB_CALLBACK
GITLAB_AUTHORIZE_URL = settings.GITLAB_AUTHORIZE_URL
GITLAB_URL = settings.GITLAB_URL

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

def gitlab_login(request):
    data = {
        'client_id': GITLAB_CLIENTID,
        'redirect_uri': GITLAB_CALLBACK,
        'response_type': 'code',
        'state': _get_refer_url(request),
    }
    gitlab_auth_url = '%s?%s'% (
        GITLAB_AUTHORIZE_URL, urllib.urlencode(data)
    )
    return HttpResponseRedirect(gitlab_auth_url)


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

def gitlab_auth(request):
    template_html = 'login/login.html'
    if 'code' not in request.GET:
        return render(request, template_html)
    code = request.GET.get('code')
    back_path = request.GET.get('state')
    url = '%s%s' % (GITLAB_URL, 'oauth/token')
    data = {
        'client_id': GITLAB_CLIENTID,
        'client_secret': GITLAB_CLIENTSECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': GITLAB_CALLBACK,
    }
    binary_data = urllib.urlencode(data).encode('utf-8')
    headers = {'Accep': 'application/json'}
    req = urllib2.Request(url, binary_data, headers)
    response = urllib2.urlopen(req)
    result = json.loads(response.read())
    access_token = result['access_token']
    url = "%s%s?access_token=%s" % (GITLAB_URL,'api/v3/user', access_token)
    response = urllib2.urlopen(url)
    data = json.loads(response.read().decode('ascii'))
    request.session['username'] = data['username']
    request.session['is_authenticated'] = True
    # 在这里处理数据库存储问题
    if back_path.startswith('/xromate'):
        #向Xromate数据库查询用户，如果没有，添加用户．如果存在，目前什么也不做
        try:
            user = Users.objects.get(username=data['username'])
        except Users.DoesNotExist:
            user = Users.objects.create(username = data['username'])
            user.save()
    elif back_path.startswith('/monitor'):
        '''
        向Monitor数据库查询用户，如果没有，添加用户．如果存在，目前什么也不做
        '''
        pass
    else:
        pass
    return HttpResponseRedirect(back_path)


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

