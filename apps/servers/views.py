from django.views.generic import ListView

from servers.models import Server

class DNSView(ListView):
    template_name = 'servers/dns'
    model = Server

    def render_to_response(self, *args, **kwargs):
        return super(DNSView, self).render_to_response(*args,
                mimetype='text/plain', **kwargs)

