from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^study/index/$', views.study_index, name='xromate_study_index'),
    url(r'^index/$', views.index, name='xromate_index'),
    url(r'^profile/$', views.profile, name='xromate_profile'),
    url(r'users/$', views.users_retrieve, name='xromate_users_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/$', views.projects_retrieve, name='xromate_projects_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/$', views.projects_flowcells_retrieve, name='xromate_projects_flowcells_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samplescount', views.samples_count, name='xromate_samples_count'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samples/(?P<sample>[^/]+)/cnvs/count', views.sample_cnvs_count, name='xromate_sample_cnvs_count'),
]
