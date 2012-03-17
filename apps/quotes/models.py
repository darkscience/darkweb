from django.db import models

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

class VoteLog(models.Model):
    quote = models.ForeignKey(Quote)
    identifier = models.CharField(max_length=40)

