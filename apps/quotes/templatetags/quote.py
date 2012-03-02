from django import template
from quotes.models import Line

register = template.Library()

@register.simple_tag
def random_quote_line():
    return Line.objects.order_by('?')[0]

