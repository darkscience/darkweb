import re

from django.http import HttpResponse

UA_BOT_REGEX = re.compile(r'bot|alexa|yandex|baidu|archive|bot|seo|crawl|spider|yahoo|msn|wget|curl', flags=re.IGNORECASE)
CONTENT_SENSITIVE_REGEX = re.compile(r'<!-- sensitive -->', flags=re.IGNORECASE)

class RobotsMiddleware(object):
    def is_bot(self, request):
        if 'HTTP_USER_AGENT' in request.META:
            return bool(UA_BOT_REGEX.search(request.META['HTTP_USER_AGENT']))
        return False

    def process_request(self, request):
        if self.is_bot(request) and (request.path.startswith('/quotes') or
                request.path.startswith('/forum')):
            return HttpResponse()

    def process_response(self, request, response):
        if self.is_bot(request) and CONTENT_SENSITIVE_REGEX.search(response.content):
            return HttpResponse()
        return response
