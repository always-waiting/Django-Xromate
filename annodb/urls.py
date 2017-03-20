from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='annodb_index'),
    url(r'^dgv/$', views.dgv, name='annodb_dgv'),
    url(r'^ucscrefgene/$', views.ucscrefgene, name='annodb_ucscrefgene'),
    url(r'^omimgenemap/$', views.omimgenemap, name='annodb_omimgenemap'),
    url(r'^omimmorbidmap/$', views.omimmorbidmap, name='annodb_omimmorbidmap'),
]
