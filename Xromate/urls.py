from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^study/index/$', views.study_index, name='xromate_study_index'),
    url(r'^index/$', views.index, name='xromate_index'),
    url(r'^projects/(?P<project>.+)/$', views.projects, name='xromate_projects'),
]
