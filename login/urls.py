from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='web_login'),
    url(r'github_login', views.github_login, name='github_login'),
    url(r'github_auth', views.github_auth, name='github_auth'),
    url(r'logout', views.logout, name='web_logout')
]
