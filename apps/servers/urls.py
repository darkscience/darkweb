from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView

from servers.views import DNSView
from servers.models import Server

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=Server.objects.filter(provides_irc=True))),
    url(r'^dns$', DNSView.as_view()),
)

