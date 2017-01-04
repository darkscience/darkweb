import re
from django.db import models

MESSAGE_REGEX = re.compile(r'(\[?[\d\:]+\]?\s+)?\<?[~&@%+\s]?(?P<sender>[\S]+)\s*[\>\:\|] (?P<message>.+)')
ACTION_REGEX =  re.compile(r'(\[?[\d\:]+\]?)?(\s+\*( \|)?)? (?P<sender>[\w\d]+) (?P<message>.+)')

class Quote(models.Model):
    votes = models.IntegerField(default=0)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.id

    def get_absolute_url(self):
        return '/quotes/%s/' % self.id

    def to_dict(self):
        return {
            "pk": self.pk,
            "votes": self.votes,
            "upload_time": self.upload_time.isoformat(),
            "lines": [],
            "url": self.get_absolute_url(),
            "upvote_url": self.get_absolute_url() + 'up/',
            "downvote_url": self.get_absolute_url() + 'down/',
            "lines": [line.to_dict() for line in self.line_set.all()]
        }


class Line(models.Model):
    sender = models.CharField(max_length=16)
    message = models.CharField(max_length=500)
    is_action = models.BooleanField(default=False)

    quote = models.ForeignKey(Quote)

    def __unicode__(self):
        if self.is_action:
            return '* %s %s' % (self.sender, self.message)
        return '<%s> %s' % (self.sender, self.message)

    class Meta:
        ordering = ['id']

    @classmethod
    def parse(cls, line):
        m = ACTION_REGEX.match(line)
        if m:
            return cls(is_action=True, **m.groupdict())

        m = MESSAGE_REGEX.match(line)
        if m:
            return cls(**m.groupdict())

        raise ValueError("Line parse failure %s" % line)

    def to_dict(self):
        return {
            'pk': self.pk,
            'sender': self.sender,
            'message': self.message,
            'is_action': self.is_action,
            'str': unicode(self),
        }


class VoteLog(models.Model):
    quote = models.ForeignKey(Quote)
    identifier = models.CharField(max_length=40)

