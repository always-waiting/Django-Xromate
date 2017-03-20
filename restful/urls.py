from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^annodb/dgv', views.annodb.dgv, name='api_annodb_dgv'),
    url(r'^annodb/ucscrefgene', views.annodb.ucscrefgene, name='api_annodb_ucscrefgene'),
    url(r'^annodb/omimgenemap', views.annodb.omimgenemap, name='api_anondb_omimgenemap'),
    url(r'^annodb/omimmorbidmap', views.annodb.omimmorbidmap, name='api_annodb_omimmorbidmap'),
    url(r'^annodb/deciphercnv', views.annodb.deciphercnv, name='api_annodb_deciphercnv'),
]
