from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from app import engine, log, Application

app = Application()

class Base(object):
    id = Column(Integer, primary_key=True)

    def save(self, session):
        session.add(self)
        log.debug("SAVING OBJECT %s COMPLETE", self.id)


Base = declarative_base(cls=Base)

class Report(Base):
    __tablename__ = app.TableConfig.report_table_name
    filename = Column(String)
    import_date = Column(DateTime, server_default=func.now())
    user = Column(String)
    type = Column(String)

    def save(self, session):
        session.add(self)
        session.commit()

class KeywordBidReportItem(Base):
    __tablename__ = app.TableConfig.keyword_bid_report_table_name
    report_id = Column(Integer, ForeignKey(Report.id))
    report_date = Column(String)
    campaign_name = Column(String)
    ad_group_name = Column(String)
    keyword = Column(String)
    currency = Column(String)
    maximum_cpc_bid = Column(String)
    ext_page_1_bid = Column(String)

class AutoKeywordReportItem(Base):
    __tablename__ = app.TableConfig.auto_keyword_report_table_name
    report_id = Column(Integer, ForeignKey(Report.id))
    campaign_name = Column(String)
    ad_group_name = Column(String)
    ad_sku = Column(String)
    customer_search_term = Column(String)
    first_day_of_impression = Column(String)
    last_day_of_impression = Column(String)
    impressions = Column(Integer)
    clicks = Column(Integer)
    ctr = Column(String)
    total_spend = Column(String)
    average_cpc = Column(String)
    currency = Column(String)
    orders_placed_within_1_week_of_click = Column(Integer)
    product_sales_within_1_week_of_click = Column(String)
    conversion_sales_within_1_week_of_click = Column(String)
    same_sku_units_ordered_within_1_week_of_click = Column(Integer)
    other_sku_units_ordered_within_1_week_of_click = Column(Integer)
    same_sku_units_product_sales_within_1_week_of_click = Column(String)
    other_sku_units_product_sales_within_1_week_of_click = Column(String)

class CampaignPerformanceReportItem(Base):
    __tablename__ = app.TableConfig.campaign_performance_report_table_name
    report_id = Column(Integer, ForeignKey(Report.id))
    campaign_name = Column(String)
    ad_group_name = Column(String)
    advertised_sku = Column(String)
    keyword = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    clicks = Column(Integer)
    impressions = Column(Integer)
    ctr = Column(String)
    total_spend = Column(String)
    average_cpc = Column(String)
    currency = Column(String)
    day_orders_placed = Column(Integer)
    day_ordered_product_sales = Column(String)
    day_conversion_rate = Column(String)
    day_same_sku_units_ordered = Column(Integer)
    day_other_sku_units_ordered = Column(Integer)
    day_same_sku_units_ordered_product_sales = Column(String)
    day_other_sku_units_ordered_product_sales = Column(String)
    week_orders_placed = Column(Integer)
    week_ordered_product_sales = Column(String)
    week_conversion_rate = Column(String)
    week_same_sku_units_ordered = Column(Integer)
    week_other_sku_units_ordered = Column(Integer)
    week_same_sku_units_ordered_product_sales = Column(String)
    week_other_sku_units_ordered_product_sales = Column(String)
    month_orders_placed = Column(Integer)
    month_ordered_product_sales = Column(String)
    month_conversion_rate = Column(String)
    month_same_sku_units_ordered = Column(Integer)
    month_other_sku_units_ordered = Column(Integer)
    month_same_sku_units_ordered_product_sales = Column(String)
    month_other_sku_units_ordered_product_sales= Column(String)

class DailySkuPerformanceReportItem(Base):
    __tablename__ = app.TableConfig.daily_sku_performance_report_table_name
    report_id = Column(Integer, ForeignKey(Report.id))
    start_date = Column(String)
    end_date = Column(String)
    merchant_name = Column(String)
    sku = Column(String)
    clicks = Column(Integer)
    impressions = Column(Integer)
    ctr = Column(String)
    currency = Column(String)
    total_spend = Column(String)
    avg_cpc = Column(String)
