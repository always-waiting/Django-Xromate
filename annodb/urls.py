from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='annodb_index'),
    url(r'^dgv/$', views.dgv, name='annodb_dgv')
]
