from django.conf.urls.defaults import patterns, include, url

from servers.views import ServerListView, DNSView
from servers.models import Server

urlpatterns = patterns('',
    url(r'^$', ServerListView.as_view()),
    url(r'^dns$', DNSView.as_view()),
)

