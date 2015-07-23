from .regex import REGEX
from .base import BasicParser
from ..models import DailySkuPerformanceReportItem

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
        item = {
            "report_id": self.report.id,
            "start_date": match.group(1),
            "end_date": match.group(2),
            "merchant_name": match.group(3),
            "sku": match.group(4),
            "clicks": int(match.group(5)),
            "impressions": int(match.group(6)),
            "ctr": match.group(7),
            "currency": match.group(8),
            "total_spend": match.group(9),
            "avg_cpc": match.group(10),
        }

        self.insert_dict(item)
        return

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
