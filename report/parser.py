import re
import os


from models import Report, AutoKeywordReportItem, KeywordBidReportItem, CampaignPerformanceReportItem, DailySkuPerformanceReportItem

from app import log, Session

class ParseError(Exception):
    """
    These are raised when there is an error in the input file
    """
    pass

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

class BasicParser(object):
    FIRST_REGEX = "^.*$"
    LINE_REGEX = "^.*$"

    def __init__(self):
        self.session = Session()
        log.debug("COMPILING %s", self.FIRST_REGEX)
        self._first_regex = re.compile(self.FIRST_REGEX)
        log.debug("COMPILING %s", self.LINE_REGEX)
        self._line_regex = re.compile(self.LINE_REGEX)

    def cleanup(self):
        self.session.close()

    def parse(self, fqn, user, catch_errors):
        """
        Take a filepath and split process it line by line
        """

        self.filename = fqn
        self.user = user


        with open(fqn) as f:
            for number, line in enumerate(f):
                if number==0:
                    try:
                        self.process_first(line.strip())
                    except ParseError:
                        log.error("INVALID FILE HEADER IN: %s", fqn)
                        if not catch_errors:
                            raise
                        break
                else:
                    try:
                        log.debug("### BEGIN LINE ###")
                        self.process_line(line.strip())
                        log.debug("### END LINE ###")
                    except ParseError:
                        log.error("INVALID LINE: %s:%d", fqn, number)
                        if not catch_errors:
                            raise

        self.cleanup()

    def process_first(self, line):
        """
        We need to validate the headers of each file and we also dont want to add the headers to the database
        """
        match = self._first_regex.match(line)
        log.debug("PROCESSING FIRST LINE: %s", line)

        if match:
            self.process_validated_first(line)

        else:
            raise ParseError("Invalid Header")

    def process_validated_first(self, line):
        """
        Create a report object
        """
        log.info("CREATING REPORT {} OBJECT FOR {}".format(self.TYPE, self.user))
        self.report = Report()
        self.report.filename = self.filename
        self.report.user = self.user
        self.report.type = self.TYPE
        self.report.save(self.session)

    def process_line(self, line):
        """
        We need to validate each line
        """
        match = self._line_regex.match(line)
        log.debug("PROCESSING LINE: %s", line)

        if match:
            self.process_validated_line(line, match)
        else:
            raise ParseError("Invalid Line")

    def process_validated_line(self, line, match):
        """
        Base class doesn't do anything with the parsed data
        """
        print line


class REGEX:
    date = r"(\d{4}-\d{2}-\d{2} [A-Z]{3})"
    datetime = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3})"
    datetime2 = r"(\d{2}\/\d{2}\/\d{4} \d{1,2}:\d{2})"
    datetime3 = r"(\d{2}\/\d{2}\/\d{4})"
    string_with_space = r"([\S ]*)"
    string = r"(\S*)"
    sku = r"([A-Z0-9]*)"
    integer = r"(\d+)"
    currency = r"([A-Z]{3})"
    float = r"(\d+\.\d+)"

    @staticmethod
    def join(list, sep=None):
        return sep.join(list)

class AutoKeywordReportParser(BasicParser):
    TYPE = "auto-keyword-report"

    FIRST_REGEX = REGEX.join([
        "Campaign Name",
        "Ad Group Name",
        "Ad \(SKU\)",
        "Customer Search Term",
        "First Day of Impression",
        "Last Day of Impression",
        "Impressions",
        "Clicks",
        "CTR",
        "Total Spend",
        "Average CPC",
        "Currency",
        "Orders placed within 1-week of a click",
        "Product Sales within 1-week of a click",
        "Conversion Rate within 1-week of a click",
        "Same SKU units Ordered within 1-week of click",
        "Other SKU units Ordered within 1-week of click",
        "Same SKU units Product Sales within 1-week of click",
        "Other SKU units Product Sales within 1-week of click",
    ], '\t')

    LINE_REGEX = REGEX.join([
        REGEX.string_with_space,
        REGEX.string_with_space,
        REGEX.sku,
        REGEX.string_with_space,
        REGEX.datetime3,
        REGEX.datetime3,
        REGEX.integer,
        REGEX.integer,
        REGEX.string,
        REGEX.float,
        REGEX.float,
        REGEX.currency,
        REGEX.string,
        REGEX.float,
        REGEX.string,
        REGEX.integer,
        REGEX.integer,
        REGEX.float,
        REGEX.float,
        #".*"
    ], '\t')

    def process_validated_line(self, line, match):
        """
        Create a AutoKeywordReportItem object from the result of parsing
        """
        item = AutoKeywordReportItem()
        item.report_id = self.report.id
        item.campaign_name = match.group(1)
        item.ad_group_name = match.group(2)
        item.ad_sku = match.group(3)
        item.customer_search_term = match.group(4)
        item.first_day_of_impression = match.group(5)
        item.last_day_of_impression = match.group(6)
        item.impressions = int(match.group(7))
        item.clicks = int(match.group(8))
        item.ctr = match.group(9)
        item.total_spend = match.group(10)
        item.average_cpc = match.group(11)
        item.currency = match.group(12)
        item.orders_placed_within_1_week_of_click = int(match.group(13))
        item.product_sales_within_1_week_of_click = match.group(14)
        item.conversion_sales_within_1_week_of_click = match.group(15)
        item.same_sku_units_ordered_within_1_week_of_click = int(match.group(16))
        item.other_sku_units_ordered_within_1_week_of_click = int(match.group(17))
        item.same_sku_units_product_sales_within_1_week_of_click = match.group(18)
        item.other_sku_units_product_sales_within_1_week_of_click = match.group(19)
        item.save(self.session)


class DailySkuPerformanceReportParser(BasicParser):
    TYPE = "daily-sku-performance-report"
    FIRST_REGEX = REGEX.join([
        "Start Date",
        "End Date",
        "Merchant Name",
        "SKU",
        "Clicks",
        "Impressions",
        "CTR",
        "Currency",
        "Total Spend",
        "Avg\. CPC"
    ], '\t')
    LINE_REGEX = REGEX.join([
            REGEX.datetime,
            REGEX.datetime,
            REGEX.string_with_space,
            REGEX.sku,
            REGEX.integer,
            REGEX.integer,
            REGEX.float,
            REGEX.currency,
            REGEX.float,
            REGEX.string
        ], '\t')
    #LINE_REGEX = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3})\t(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3})\t([_a-zA-Z 0-9\-]*)\t([A-Z0-9]*)\t(\d+)\t(\d+)\t(\d+\.\d{2,})\t([A-Z]{3})\t(\d+\.\d{2})\t(\S+)"


    def process_validated_line(self, line, match):
        """
        Create a DailySkuPerformanceReportItem
        """

        item = DailySkuPerformanceReportItem()
        item.report_id = self.report.id
        item.start_date = match.group(1)
        item.end_date = match.group(2)
        item.merchant_name = match.group(3)
        item.sku = match.group(4)
        item.clicks = int(match.group(5))
        item.impressions = int(match.group(6))
        item.ctr = match.group(7)
        item.currency = match.group(8)
        item.total_spend = match.group(9)
        item.avg_cpc = match.group(10)
        item.save(self.session)

class KeywordBidReportParser(BasicParser):
    TYPE = "keyword-bid-report"
    FIRST_REGEX = REGEX.join([
        "Report Date",
        "Campaign Name",
        "Ad Group Name",
        "Keyword",
        "Currency",
        "Your Maximum CPC Bid",
        "Est Page 1 Bid"
    ], '\t')
    LINE_REGEX = REGEX.join([
            REGEX.date,
            REGEX.string_with_space,
            REGEX.string_with_space,
            REGEX.string_with_space,
            REGEX.currency,
            REGEX.float,
            REGEX.string
        ], '\t')
    #LINE_REGEX = r"(\d{4}-\d{2}-\d{2} [A-Z]{3})\t([_a-zA-Z 0-9\-]*)\t([_a-zA-Z 0-9\-]*)\t([_a-zA-Z 0-9\-]*)\t([A-Z]{3})\t(\d+\.\d{2})\t(\S+)"

    def process_validated_line(self, line, match):
        """
        Create a KeywordBidReportItem
        """
        item = KeywordBidReportItem()
        item.report_id = self.report.id
        item.report_date = match.group(1)
        item.campaign_name = match.group(2)
        item.ad_group_name = match.group(3)
        item.keyword = match.group(4)
        item.currency = match.group(5)
        item.maximum_cpc_bid = match.group(6)
        item.ext_page_1_bid = match.group(7)
        item.save(self.session)

class CampaignPerformanceReporParser(BasicParser):
    TYPE = "campaign-performance-report"
    FIRST_REGEX = REGEX.join([
        "Campaign Name",
        "Ad Group Name",
        "Advertised SKU",
        "Keyword",
        "Start Date",
        "End Date",
        "Clicks",
        "Impressions",
        "CTR",
        "Total Spend",
        "Average CPC",
        "Currency",
        "1-day Orders Placed \(#\)",
        "1-day Ordered Product Sales \(\$\)",
        "1-day Conversion Rate",
        "1-day Same SKU Units Ordered",
        "1-day Other SKU Units Ordered",
        "1-day Same SKU Units Ordered Product Sales",
        "1-day Other SKU Units Ordered Product Sales",
        "1-week Orders Placed \(#\)",
        "1-week Ordered Product Sales \(\$\)",
        "1-week Conversion Rate",
        "1-week Same SKU Units Ordered",
        "1-week Other SKU Units Ordered",
        "1-week Same SKU Units Ordered Product Sales",
        "1-week Other SKU Units Ordered Product Sales",
        "1-month Orders Placed \(#\)",
        "1-month Ordered Product Sales \(\$\)",
        "1-month Conversion Rate",
        "1-month Same SKU Units Ordered",
        "1-month Other SKU Units Ordered",
        "1-month Same SKU Units Ordered Product Sales",
        "1-month Other SKU Units Ordered Product Sales"
    ], '\t')
    LINE_REGEX = REGEX.join([
        REGEX.string_with_space,
        REGEX.string_with_space,
        REGEX.sku,
        REGEX.string_with_space,
        REGEX.datetime2,
        REGEX.datetime2,
        REGEX.integer,
        REGEX.integer,
        REGEX.string,
        REGEX.float,
        REGEX.string,
        REGEX.currency,
        REGEX.integer,
        REGEX.float,
        REGEX.string,
        REGEX.integer,
        REGEX.integer,
        REGEX.float,
        REGEX.float,
        REGEX.integer,
        REGEX.float,
        REGEX.string,
        REGEX.integer,
        REGEX.integer,
        REGEX.float,
        REGEX.float,
        REGEX.integer,
        REGEX.float,
        REGEX.string,
        REGEX.integer,
        REGEX.integer,
        REGEX.float,
        REGEX.float
    ], '\t')

    def process_validated_line(self, line, match):
        """
        Create a CampaignPerformanceReportItem
        """
        item = CampaignPerformanceReportItem()
        item.report_id = self.report.id
        item.campaign_name = match.group(1)
        item.ad_group_name = match.group(2)
        item.advertised_sku = match.group(3)
        item.keyword = match.group(4)
        item.start_date = match.group(5)
        item.end_date = match.group(6)
        item.clicks = int(match.group(7))
        item.impressions = int(match.group(8))
        item.ctr = match.group(9)
        item.total_spend = match.group(10)
        item.average_cpc = match.group(11)
        item.currency = match.group(12)
        item.day_orders_placed = int(match.group(13))
        item.day_ordered_product_sales = match.group(14)
        item.day_conversion_rate = match.group(15)
        item.day_same_sku_units_ordered = int(match.group(16))
        item.day_other_sku_units_ordered = int(match.group(17))
        item.day_same_sku_units_ordered_product_sales = match.group(18)
        item.day_other_sku_units_ordered_product_sales = match.group(19)
        item.week_orders_placed = int(match.group(20))
        item.week_ordered_product_sales = match.group(21)
        item.week_conversion_rate = match.group(22)
        item.week_same_sku_units_ordered = int(match.group(23))
        item.week_other_sku_units_ordered = int(match.group(24))
        item.week_same_sku_units_ordered_product_sales = match.group(25)
        item.week_other_sku_units_ordered_product_sales = match.group(26)
        item.month_orders_placed = int(match.group(27))
        item.month_ordered_product_sales = match.group(28)
        item.month_conversion_rate = match.group(29)
        item.month_same_sku_units_ordered = int(match.group(30))
        item.month_other_sku_units_ordered = int(match.group(31))
        item.month_same_sku_units_ordered_product_sales = match.group(32)
        item.month_other_sku_units_ordered_product_sales = match.group(33)
        item.save(self.session)



parser.register_parser(AutoKeywordReportParser.TYPE, AutoKeywordReportParser)
parser.register_parser(DailySkuPerformanceReportParser.TYPE, DailySkuPerformanceReportParser)
parser.register_parser(KeywordBidReportParser.TYPE, KeywordBidReportParser)
parser.register_parser(CampaignPerformanceReporParser.TYPE, CampaignPerformanceReporParser)
