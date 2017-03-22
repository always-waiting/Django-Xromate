from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^annodb/(?P<table>.+)/(?P<locs>[\d|X|Y]+:\d+-\d+)/$', views.annodb.table_locs, name='api_annodb_table_locs'),
]
