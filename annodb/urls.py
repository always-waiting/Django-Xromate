from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='annodb_index'),
    url(r'(?P<table>.+)/(?P<locs>[\d|X|Y]+:\d+-\d+)/', views.table_locs, name='annodb_table_locs'),
]
