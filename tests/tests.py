import unittest
import re
import os

from report.parser import REGEX, parser, ParseError
from report.app import Application

class TestRegularExpressions(unittest.TestCase):
    def test_date(self):
        test_string = "1992-05-29 PDT"
        self.assertIsNotNone(re.match(REGEX.date, test_string))

    def test_datetime(self):
        test_string = "1992-05-29 10:36:23 PDT"
        self.assertIsNotNone(re.match(REGEX.datetime, test_string))

    def test_datetime2(self):
        test_string = "05/29/1992 1:23"
        self.assertIsNotNone(re.match(REGEX.datetime2, test_string))

    def test_datetime3(self):
        test_string = "05/29/1992"
        self.assertIsNotNone(re.match(REGEX.datetime3, test_string))

    def test_string_with_space(self):
        test_string = "Hello World! This 1s c0w_."
        self.assertIsNotNone(re.match(REGEX.string_with_space, test_string))

    def test_string(self):
        test_string = "Hell0!"
        self.assertIsNotNone(re.match(REGEX.string, test_string))

    def test_sku(self):
        test_string = "EEKEL4923E"
        self.assertIsNotNone(re.match(REGEX.sku, test_string))

    def test_integer(self):
        test_string = "1234"
        self.assertIsNotNone(re.match(REGEX.integer, test_string))

    def test_currncy(self):
        test_string = "USD"
        self.assertIsNotNone(re.match(REGEX.currency, test_string))

    def test_float(self):
        test_string = "1.222123"
        self.assertIsNotNone(re.match(REGEX.float, test_string))

#class SampleFileTests(unittest.TestCase):
#
#    def setUp(self):
#        from report import create_db
#
#    @staticmethod
#    def filename(fn):
#        return os.path.abspath(fn)
#
#    def test_autokeyword_report(self):
#        try:
#            parser.parse(self.filename('data/auto-keyword-report-2015-04-30-50651016615.txt'), catch_errors=False)
#        except ParseError as e:
#            self.fail(str(e))
#
#    def test_campaign_performance_report(self):
#        try:
#            parser.parse(self.filename('data/campaign-performance-report-2015-04-30-50650016615.txt'), catch_errors=False)
#        except ParseError as e:
#            self.fail(str(e))
#
#    def test_daily_sku_performance_report(self):
#        try:
#            parser.parse(self.filename('data/daily-sku-performance-report-2015-04-28-12061537256.txt'), catch_errors=False)
#        except ParseError as e:
#            self.fail(str(e))
#
#    def test_keyword_bid_report(self):
#        try:
#            parser.parse(self.filename('data/keyword-bid-report-2015-05-21-50373016577.txt'), catch_errors=False)
#        except ParseError as e:
#            self.fail(str(e))

if __name__ == "__main__":
    app = Application()
    app.setup()
    app.create_db()
    unittest.main()
