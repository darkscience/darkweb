from django.test import TestCase
from quotes.models import Line


class SimpleTest(TestCase):
    def check_message(self, line):
        line = Line.parse(line)
        self.assertEqual(line.sender, 'kylef')
        self.assertEqual(line.message, 'hi there')
        self.assertEqual(line.is_action, False)

    def check_action(self, line):
        line = Line.parse(line)
        self.assertEqual(line.sender, 'kylef')
        self.assertEqual(line.message, 'loves github')
        self.assertEqual(line.is_action, True)

    def test_line_parse_irssi_message(self):
        self.check_message('18:00 <kylef> hi there')

    def test_line_parse_irssi_action(self):
        self.check_action('18:00  * kylef loves github')

    def test_line_parse_textual_message(self):
        self.check_message('[18:06:49] <~kylef> hi there')

    def test_line_parse_textual_action(self):
        self.check_action('[18:07:08] kylef loves github')

