from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

ROBOTS = """User-agent: *
Disallow: /quotes/
"""

def error_view(request):
    raise Exception('Test exception')

urlpatterns = patterns('',
    url(r'^quotes/', include('quotes.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', lambda r: HttpResponse(ROBOTS, mimetype="text/plain")),
    url(r'^500/$', error_view),
)
