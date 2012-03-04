from django import template
from django.utils.html import escape
from quotes.models import Line

register = template.Library()

@register.simple_tag
def random_quote_line():
    return escape(Line.objects.order_by('?')[0])

