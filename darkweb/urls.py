from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

ROBOTS = """User-agent: *
Disallow: /quotes/
Disallow: /forum/
"""

urlpatterns = patterns('',
    url(r'^forum/', include('lithium.forum.urls')),
    url(r'^wiki/', include('lithium.wiki.urls')),
    # Examples:
    # url(r'^$', 'darkweb.views.home', name='home'),
    # url(r'^darkweb/', include('darkweb.foo.urls')),
    url(r'^quotes/', include('quotes.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^servers/', include('servers.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', lambda r: HttpResponse(ROBOTS, mimetype="text/plain")),
)
