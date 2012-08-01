from django.contrib import admin
from servers.models import Tag, Server

class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'ipv4', 'ipv6',)

    fieldsets = (
        (None, {
            'fields': ('name', 'owner', 'location'),
        }),
        ('Status', {
            'fields': ('is_online', 'tags'), 
        }),
        ('Addresses', {
            'fields': ('ipv4', 'ipv6', 'tor'),
        }),
    )

admin.site.register(Tag)
admin.site.register(Server, ServerAdmin)

