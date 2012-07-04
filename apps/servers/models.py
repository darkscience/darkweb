from django.db import models
from django.contrib.auth.models import User

from servers.utils import COUNTRIES

class Server(models.Model):
    name = models.CharField(max_length=16)
    owner = models.ForeignKey(User)
    location = models.CharField(max_length=2, choices=COUNTRIES)

    ipv4 = models.GenericIPAddressField(verbose_name='IPv4', protocol='ipv4',
            blank=True, null=True)
    ipv6 = models.GenericIPAddressField(verbose_name='IPv6', protocol='ipv6',
            blank=True, null=True)

    tor = models.CharField(max_length=64, blank=True)

    fingerprint = models.CharField(max_length=40, help_text='SSL Fingerprint')

    provides_irc = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def domain(self):
        return u'%s.darkscience.net' % self.name
