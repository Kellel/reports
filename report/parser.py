import re
import os


from models import Report, AutoKeywordReportItem, KeywordBidReportItem, CampaignPerformanceReportItem, DailySkuPerformanceReportItem

from app import log, application

from parsers import ParseError, AutoKeywordReportParser, DailySkuPerformanceReportParser, KeywordBidReportParser, CampaignPerformanceReportParser

class ParserManager(object):
    def __init__(self):
        self.parsers = {}

    def register_parser(self, type, cls):
        self.parsers[type] = cls()

    def deregister_parser(self, type):
        del self.parsers[type]

    def parse(self, filename, user, catch_errors=True):
        fn = os.path.basename(filename)
        log.debug("GOT %s", filename)

        for type,parser in self.parsers.items():
            if fn.startswith(type):
                log.debug("PARSER MATCHED %s == %s", type, fn)
                parser.parse(filename, user, catch_errors)
                return
        raise ParseError("No valid parser found.")

# Import and use this please
parser = ParserManager()
parser.register_parser(AutoKeywordReportParser.TYPE, AutoKeywordReportParser)
parser.register_parser(DailySkuPerformanceReportParser.TYPE, DailySkuPerformanceReportParser)
parser.register_parser(KeywordBidReportParser.TYPE, KeywordBidReportParser)
parser.register_parser(CampaignPerformanceReportParser.TYPE, CampaignPerformanceReportParser)
