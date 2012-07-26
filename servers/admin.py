from django.contrib import admin
from servers.models import Server

class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'ipv4', 'ipv6',)

    fieldsets = (
        (None, {
            'fields': ('name', 'owner', 'fingerprint', 'location'),
        }),
        ('Status', {
            'fields': ('provides_irc', 'is_online'), 
        }),
        ('Addresses', {
            'fields': ('ipv4', 'ipv6', 'tor'),
        }),
    )

admin.site.register(Server, ServerAdmin)

