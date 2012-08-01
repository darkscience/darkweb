from django.views.generic import ListView

from servers.models import Server

class ServerListView(ListView):
    queryset = Server.objects.filter(tags__name='irc')
    
class DNSView(ListView):
    template_name = 'servers/dns'
    model = Server

    def render_to_response(self, *args, **kwargs):
        return super(DNSView, self).render_to_response(*args,
                mimetype='text/plain', **kwargs)

