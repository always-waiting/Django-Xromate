from django.conf.urls import url

#from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^study/index/$', views.study_index, name='xromate_study_index'),
    url(r'^index/$', views.index, name='xromate_index'),
    url(r'^profile/$', views.profile, name='xromate_profile'),
    url(r'users/$', views.users_retrieve, name='xromate_users_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/$', views.projects_retrieve, name='xromate_projects_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/$', views.projects_flowcells_retrieve, name='xromate_projects_flowcells_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samplescount', views.samples_count, name='xromate_samples_count'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samples/(?P<sample>[^/]+)/cnvs/count$', views.sample_cnvs_count, name='xromate_sample_cnvs_count'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samples/(?P<sample>[^/]+)$', views.projects_flowcells_samples_retrieve, name='xromate_projects_flowcells_samples_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samples/(?P<sample>[^/]+)/remotes/remote$', views.project_flowcell_sample_remote_retrieve, name='xromate_project_flowcell_sample_remote_retrieve'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samples/(?P<sample>[^/]+)/chromosomes$', views.project_flowcell_sample_chromosomes_list, name='xromate_project_flowcell_sample_chromosomes_list'),
    url(r'^projects/(?P<project>[^/]+)/flowcells/(?P<flowcell>[^/]+)/samples/(?P<sample>[^/]+)/chromosomes/(?P<chrom>[^/.]+)(?:.(?P<format>[a-zA-Z]+))?$', views.project_flowcell_sample_chromosome_retrieve, name='xromate_project_flowcell_sample_chromosome_retrieve'),
]


#urlpatterns = format_suffix_patterns(urlpatterns)
