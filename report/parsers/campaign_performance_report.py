from .regex import REGEX
from .base import BasicParser
from ..models import CampaignPerformanceReportItem

class CampaignPerformanceReportParser(BasicParser):
    TYPE = "campaign-performance-report"
    DB_CLS = CampaignPerformanceReportItem
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
        item = {
            "report_id": self.report.id,
            "campaign_name": match.group(1),
            "ad_group_name": match.group(2),
            "advertised_sku": match.group(3),
            "keyword": match.group(4),
            "start_date": match.group(5),
            "end_date": match.group(6),
            "clicks": int(match.group(7)),
            "impressions": int(match.group(8)),
            "ctr": match.group(9),
            "total_spend": match.group(10),
            "average_cpc": match.group(11),
            "currency": match.group(12),
            "day_orders_placed": int(match.group(13)),
            "day_ordered_product_sales": match.group(14),
            "day_conversion_rate": match.group(15),
            "day_same_sku_units_ordered": int(match.group(16)),
            "day_other_sku_units_ordered": int(match.group(17)),
            "day_same_sku_units_ordered_product_sales": match.group(18),
            "day_other_sku_units_ordered_product_sales": match.group(19),
            "week_orders_placed": int(match.group(20)),
            "week_ordered_product_sales": match.group(21),
            "week_conversion_rate": match.group(22),
            "week_same_sku_units_ordered": int(match.group(23)),
            "week_other_sku_units_ordered": int(match.group(24)),
            "week_same_sku_units_ordered_product_sales": match.group(25),
            "week_other_sku_units_ordered_product_sales": match.group(26),
            "month_orders_placed": int(match.group(27)),
            "month_ordered_product_sales": match.group(28),
            "month_conversion_rate": match.group(29),
            "month_same_sku_units_ordered": int(match.group(30)),
            "month_other_sku_units_ordered": int(match.group(31)),
            "month_same_sku_units_ordered_product_sales": match.group(32),
            "month_other_sku_units_ordered_product_sales": match.group(33),
        }

        self.insert_dict(item)
        return
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

