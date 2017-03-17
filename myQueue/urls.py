from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='myqueue_index'),
    url(r'^fid/$', views.fid_get, name='myqueue_fid'),
    url(r'^fid/pop$', views.fid_delete, name='myqueue_fid_pop')
]

