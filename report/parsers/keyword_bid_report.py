from .regex import REGEX
from .base import BasicParser
from ..models import KeywordBidReportItem

class KeywordBidReportParser(BasicParser):
    TYPE = "keyword-bid-report"
    DB_CLS = KeywordBidReportItem
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
        item = {
            "report_id": self.report.id,
            "report_date": match.group(1),
            "campaign_name": match.group(2),
            "ad_group_name": match.group(3),
            "keyword": match.group(4),
            "currency": match.group(5),
            "maximum_cpc_bid": match.group(6),
            "ext_page_1_bid": match.group(7),
        }
        self.insert_dict(item)
        return
        #item = KeywordBidReportItem()
        #item.report_id = self.report.id
        #item.report_date = match.group(1)
        #item.campaign_name = match.group(2)
        #item.ad_group_name = match.group(3)
        #item.keyword = match.group(4)
        #item.currency = match.group(5)
        #item.maximum_cpc_bid = match.group(6)
        #item.ext_page_1_bid = match.group(7)
        #item.save(self.session)
