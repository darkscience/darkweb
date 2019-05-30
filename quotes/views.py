import hashlib
import json

from django.views.generic import FormView, RedirectView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from django.utils.cache import patch_vary_headers
from django.views.decorators.cache import cache_control
from django.views.decorators.http import condition
from django.utils.decorators import method_decorator

from quotes.models import Quote, VoteLog, Line
from quotes.forms import QuoteForm


def quotes_etag(request, *args, **kwargs):
    quotes = [quote.to_dict() for quote in Quote.objects.order_by('pk')]
    payload = json.dumps(quotes)
    return hashlib.md5(payload.encode('utf-8')).hexdigest()


def last_modified(request, *args, **kwargs):
    try:
        return Quote.objects.order_by('upload_time')[:1].get().upload_time
    except Quote.DoesNotExist:
        return


class QuoteDetail(DetailView):
    model = Quote

    def get(self, request, **kwargs):
        if 'application/json' == request.META.get('HTTP_ACCEPT', None):
            quote = self.get_object().to_dict()
            response = HttpResponse(json.dumps(quote), content_type='application/json')
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

        if 'application/json' == self.request.META.get('HTTP_ACCEPT', None):
            response = HttpResponse(json.dumps(self.object.to_dict()), content_type='application/json')
        else:
            response = super(AddQuoteView, self).form_valid(form)

        patch_vary_headers(response, ['Accept'])

        return response

class VoteView(RedirectView):#, SingleObjectMixin):
    up = True

    def vote(self, pk):
        quote = get_object_or_404(Quote, pk=pk)

        if self.request.user.is_authenticated():
            identifier = self.request.user.username
        else:
            identifier = hashlib.sha1(self.request.META['REMOTE_ADDR'].encode('utf-8')).hexdigest()

        if not VoteLog.objects.filter(quote=quote, identifier=identifier).count():
            log = VoteLog(quote=quote, identifier=identifier)

            if self.up:
                quote.votes += 1
            else:
                quote.votes -= 1

            log.save()
            quote.save()

        return quote

    def get(self, request, pk):
        if 'application/json' == request.META.get('HTTP_ACCEPT', None):
            quote = self.vote(pk)
            response = HttpResponse(json.dumps(quote.to_dict()), content_type='application/json')
        else:
            response = super(VoteView, self).get(request, pk=pk)

        patch_vary_headers(response, ['Accept'])
        return response

    def get_redirect_url(self, pk):
        quote = self.vote(pk)
        return quote.get_absolute_url()


class ListQuotes(ListView):
    queryset = Quote.objects.order_by('-pk')
    paginate_by = 5

    @method_decorator(condition(quotes_etag, last_modified))
    @method_decorator(cache_control(max_age=0))
    def get(self, request, **kwargs):
        if 'application/json' == request.META.get('HTTP_ACCEPT', None):
            quotes = self.get_queryset()
            quotes = [quote.to_dict() for quote in quotes]
            response = HttpResponse(json.dumps(quotes), content_type='application/json')
        else:
            response = super(ListQuotes, self).get(request, **kwargs)

        patch_vary_headers(response, ['Accept'])
        return response


class TopQuotes(ListQuotes):
    queryset = Quote.objects.order_by('-votes', '-pk')


class RandomQuotes(ListQuotes):
    queryset = Quote.objects.order_by('?')

