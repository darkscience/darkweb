import json

from django.views.generic import ListView
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers

from servers.models import Server

class ServerListView(ListView):
    queryset = Server.objects.filter(tags__name='irc')

    def get(self, request, *args, **kwargs):
        if request.META.get('HTTP_ACCEPT', None) == 'application/json':
            servers = [server.as_dict() for server in Server.objects.all()]
            response = HttpResponse(json.dumps(servers),
                content_type='application/json')
            add_never_cache_headers(response)
            return response

        return super(ServerListView, self).get(request, *args, **kwargs)

class DNSView(ListView):
    template_name = 'servers/dns'
    model = Server

    def render_to_response(self, *args, **kwargs):
        return super(DNSView, self).render_to_response(*args,
                mimetype='text/plain', **kwargs)

