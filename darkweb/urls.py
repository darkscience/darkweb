from django.conf.urls.defaults import patterns, include, url
from django.http import HttpResponse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

ROBOTS = """User-agent: *
Disallow: /quotes/
"""

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'darkweb.views.home', name='home'),
    # url(r'^darkweb/', include('darkweb.foo.urls')),
    url(r'^quotes/', include('quotes.urls')),

    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^servers/', include('servers.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots\.txt$', lambda r: HttpResponse(ROBOTS, mimetype="text/plain")),
)
