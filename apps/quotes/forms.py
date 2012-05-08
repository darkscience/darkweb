from django import forms

from quotes.models import Quote, Line


class QuoteForm(forms.Form):
    quote = forms.CharField(widget=forms.Textarea)

    def is_valid(self):
        result = super(QuoteForm, self).is_valid()

        if result:
            line_no = 1
            for l in self.cleaned_data['quote'].splitlines():
                try:
                    Line.parse(l)
                except ValueError:
                    if 'quote' not in self.errors:
                        self.errors['quote'] = []

                    self.errors['quote'].append('Line %s is invalid. Please ' \
                            'show the line on #darkscience for help.' % line_no)
                    result = False
                line_no += 1

        return result

    def save(self):
        lines = [Line.parse(l) for l in self.cleaned_data['quote'].splitlines()]

        quote = Quote()
        quote.save()

        for line in lines:
            line.quote = quote
            line.save()

        return quote

