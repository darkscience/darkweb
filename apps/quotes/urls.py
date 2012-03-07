from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView, FormView

from quotes.models import Quote
from quotes.views import AddQuoteView, VoteView, ListQuotes, TopQuotes, QuoteDetail, RandomQuotes

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', QuoteDetail.as_view(model=Quote)),
    url(r'^(?P<pk>\d+)/up/$', VoteView.as_view()),
    url(r'^(?P<pk>\d+)/down/$', VoteView.as_view(up=False)),
    url(r'^add/$', AddQuoteView.as_view()),
    url(r'^$', TopQuotes.as_view()),
    url(r'^all/$', ListQuotes.as_view()),
    url(r'^random/$', RandomQuotes.as_view()),
)
