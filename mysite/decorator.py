# encoding: utf-8
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def login_required(login_url):
    def _login_required(func):
        def wrapper(request):
            if 'is_authenticated' not in request.session:
                request.session['back_url'] = request.get_full_path()
                return HttpResponseRedirect(reverse('web_login'))
            elif not request.session['is_authenticated']:
                request.session['back_url'] = request.get_full_path()
                return HttpResponseRedirect(reverse('web_login'))
            else:
                return func(request)
        return wrapper
    return _login_required

