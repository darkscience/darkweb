import re
from django import forms
from quotes.models import Quote, Line

MESSAGE_REGEX = re.compile(r'(\[[\d\:]+\] )?\<?[~&@%+\s]?(?P<sender>[\S]+)[\>\:] (?P<message>.+)')
ACTION_REGEX =  re.compile(r'(\[[\d\:]+\] )?(\* )?(?P<sender>[\w\d]+) (?P<message>.+)')

class QuoteForm(forms.Form):
    quote = forms.CharField(widget=forms.Textarea)

    def is_valid(self):
        result = super(QuoteForm, self).is_valid()

        if result:
            x = 1
            for l in self.cleaned_data['quote'].splitlines():
                if not (ACTION_REGEX.match(l) or MESSAGE_REGEX.match(l)):
                    if 'quote' not in self.errors:
                        self.errors['quote'] = []
                    self.errors['quote'].append('Line %s is invalid. Please show the line on #darkscience for help.' % x)
                    result = False
                x += 1

        return result

    def save(self):
        quote = Quote()
        lines = []

        for l in self.cleaned_data['quote'].splitlines():
            line = None

            m = ACTION_REGEX.match(l)
            if m:
                line = Line(is_action=True, **m.groupdict())
            else:
                m = MESSAGE_REGEX.match(l)
                if m:
                    line = Line(**m.groupdict())

            if not line:
                raise ValueError("Line parse failure %s" % l)

            lines.append(line)

        quote.save()

        for line in lines:
            line.quote = quote
            line.save()

        return quote

