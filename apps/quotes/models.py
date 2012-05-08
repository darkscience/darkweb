import re
from django.db import models

MESSAGE_REGEX = re.compile(r'(\[[\d\:]+\] )?\<?[~&@%+\s]?(?P<sender>[\S]+)[\>\:] (?P<message>.+)')
ACTION_REGEX =  re.compile(r'(\[[\d\:]+\] )?(\* )?(?P<sender>[\w\d]+) (?P<message>.+)')

class Quote(models.Model):
    votes = models.IntegerField(default=0)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.id

    def get_absolute_url(self):
        return '/quotes/%s/' % self.id

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

class VoteLog(models.Model):
    quote = models.ForeignKey(Quote)
    identifier = models.CharField(max_length=40)

