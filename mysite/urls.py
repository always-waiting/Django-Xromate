# encoding: utf-8
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from homepage import views as homepage_views
#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',homepage_views.index, name="homepage"),
    url(r'^annodb/', include("annodb.urls")),
    url(r'^genoverse/', include("genoverse.urls")),
    url(r'^admin/', admin.site.urls),
    url(r'^myqueue/', include("myQueue.urls")),
    url(r'^api/',include("restful.urls")),
    url(r'^xromate/', include('Xromate.urls')),
    url(r'login/', include('login.urls')),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
