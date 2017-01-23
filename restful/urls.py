from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^annodb/dgv', views.annodb.dgv, name='api_annodb_dgv'),
]
