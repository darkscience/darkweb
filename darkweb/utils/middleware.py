import re

from django.http import HttpResponse

UA_BOT_REGEX = re.compile(r'bot|alexa|yandex|baidu|archive|bot|seo|crawl|spider|yahoo|msn|wget|curl', flags=re.IGNORECASE)
CONTENT_SENSITIVE_REGEX = re.compile(r'<!-- sensitive -->', flags=re.IGNORECASE)

class RobotsMiddleware(object):
    def is_bot(self, request):
        return bool(UA_BOT_REGEX.search(request.META['HTTP_USER_AGENT']))

    def process_request(self, request):
        if request.path.startswith('/quotes') and self.is_bot(request):
            return HttpResponse()

    def process_response(self, request, response):
        if self.is_bot(request) and CONTENT_SENSITIVE_REGEX.search(response.content):
            return HttpResponse()
        return response
