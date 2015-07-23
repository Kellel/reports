from .regex import REGEX
from .base import BasicParser
from ..models import AutoKeywordReportItem

class AutoKeywordReportParser(BasicParser):
    TYPE = "auto-keyword-report"
    DB_CLS = AutoKeywordReportItem

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
        dictionary = {
            'report_id': self.report.id,
            'campaign_name': match.group(1),
            'ad_group_name': match.group(2),
            'ad_sku': match.group(3),
            'customer_search_term': match.group(4),
            'first_day_of_impression': match.group(5),
            'last_day_of_impression': match.group(6),
            'impressions': int(match.group(7)),
            'clicks': int(match.group(8)),
            'ctr': match.group(9),
            'total_spend': match.group(10),
            'average_cpc': match.group(11),
            'currency': match.group(12),
            'orders_placed_within_1_week_of_click': int(match.group(13)),
            'product_sales_within_1_week_of_click': match.group(14),
            'conversion_sales_within_1_week_of_click': match.group(15),
            'same_sku_units_ordered_within_1_week_of_click': int(match.group(16)),
            'other_sku_units_ordered_within_1_week_of_click': int(match.group(17)),
            'same_sku_units_product_sales_within_1_week_of_click': match.group(18),
            'other_sku_units_product_sales_within_1_week_of_click': match.group(19)
        }

        self.insert_dict(dictionary)

        print "INSERTED TO THINGY #########"

        return

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
