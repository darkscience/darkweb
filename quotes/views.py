import hashlib
import json

from django.views.generic import FormView, RedirectView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.utils.cache import patch_vary_headers

from quotes.models import Quote, VoteLog, Line
from quotes.forms import QuoteForm

class QuoteDetail(DetailView):
    model = Quote

    def get(self, request, **kwargs):
        if 'application/json' == request.META.get('HTTP_ACCEPT', None):
            quote = self.get_object().to_dict()
            response = HttpResponse(json.dumps(quote), mimetype='application/json')
        else:
            response = super(QuoteDetail, self).get(request, **kwargs)

        patch_vary_headers(response, ['Accept'])
        return response


class RandomQuoteDetail(QuoteDetail):
    def get_object(self):
        return Quote.objects.order_by('?')[0]


class RandomQuote(QuoteDetail):
    def get_object(self):
        return self.model.objects.order_by('?')[0]

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

    def get(self, request, **kwargs):
        if 'application/json' == request.META.get('HTTP_ACCEPT', None):
            quotes = self.get_queryset()
            quotes = [quote.to_dict() for quote in quotes]
            response = HttpResponse(json.dumps(quotes), mimetype='application/json')
        else:
            response = super(QuoteDetail, self).get(request, **kwargs)

        patch_vary_headers(response, ['Accept'])
        return response


class TopQuotes(ListQuotes):
    queryset = Quote.objects.order_by('-votes', '-pk')


class RandomQuotes(ListQuotes):
    queryset = Quote.objects.order_by('?')

