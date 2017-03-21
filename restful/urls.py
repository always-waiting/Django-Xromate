from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^annodb/dgv', views.annodb.dgv, name='api_annodb_dgv'),
    url(r'^annodb/ucscrefgene', views.annodb.ucscrefgene, name='api_annodb_ucscrefgene'),
    url(r'^annodb/omimgenemap', views.annodb.omimgenemap, name='api_anondb_omimgenemap'),
    url(r'^annodb/omimmorbidmap', views.annodb.omimmorbidmap, name='api_annodb_omimmorbidmap'),
    url(r'^annodb/deciphercnv', views.annodb.deciphercnv, name='api_annodb_deciphercnv'),
    url(r'^annodb/clinvar', views.annodb.clinvar, name='api_annodb_clinvar'),
    url(r'^annodb/genereview', views.annodb.genereview, name='api_annodb_genereview'),
    url(r'^annodb/deciphersyndrome', views.annodb.deciphersyndrome, name='api_annodb_deciphersyndrome'),
    url(r'^annodb/pubmed', views.annodb.pubmed, name='api_annodb_pubmed'),
]
