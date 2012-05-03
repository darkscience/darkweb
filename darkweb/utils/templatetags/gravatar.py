import urllib, hashlib
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def gravatar(email, size=48):
    """
    Simply gets the Gravatar for the commenter. There is no rating or
    custom "not found" icon yet. Used with the Django comments.
    
    If no size is given, the default is 48 pixels by 48 pixels.
    
    Template Syntax::
    
        {% gravatar comment.user_email [size] %}
        
    Example usage::
        
        {% gravatar comment.user_email 48 %}
    """
    
    default = 'identicon'
    
    return "http://www.gravatar.com/avatar.php?" + urllib.urlencode({
        'd': 'identicon',
        'gravatar_id': hashlib.md5(email).hexdigest(),
        'size': str(size)
    })

