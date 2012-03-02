import hashlib

from django.views.generic import FormView, RedirectView, ListView
from django.shortcuts import get_object_or_404

from quotes.models import Quote, VoteLog
from quotes.forms import QuoteForm


class AddQuoteView(FormView):
    form_class = QuoteForm
    template_name = 'quotes/add_quote.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        self.object = form.save()
        return super(AddQuoteView, self).form_valid(form)

class VoteView(RedirectView):#, SingleObjectMixin):
    up = True

    def get_redirect_url(self, pk):
        quote = get_object_or_404(Quote, pk=pk)

        if self.request.user.is_authenticated():
            identifier = self.request.user.username
        else:
            identifier = hashlib.sha1(self.request.META['REMOTE_ADDR']).hexdigest()

        if not VoteLog.objects.filter(quote=quote, identifier=identifier).count():
            log = VoteLog(quote=quote, identifier=identifier)

            if self.up:
                quote.votes += 1
            else:
                quote.votes -= 1

            log.save()
            quote.save()

        return quote.get_absolute_url()

class ListQuotes(ListView):
    queryset = Quote.objects.order_by('-pk')
    paginate_by = 5

class TopQuotes(ListQuotes):
    queryset = Quote.objects.order_by('-votes')
