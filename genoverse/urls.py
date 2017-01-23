from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='genoverse_index'),
    url(r'^embed/$', views.embed, name="genoverse_embed"),
    url(r'^add_tracker', views.add_tracker, name="genoverse_add_tracker"),
]
