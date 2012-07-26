from django.contrib import admin

from quotes.models import Quote, Line

class LineAdmin(admin.StackedInline):
    model = Line

class QuoteAdmin(admin.ModelAdmin):
    inlines = [LineAdmin]

admin.site.register(Quote, QuoteAdmin)

