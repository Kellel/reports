####
#### REPORT DAEMON DEFAULT CONFIGURATION
####

# Database uri for more information lookup sqlalchemy database uri
SQLALCHEMY_URI="sqlite:///report.db"

# Change the log level of the daemon (debug, info, warning, error, critical)
LOG_LEVEL="info"

# enable database logging. This will print out every db transaction that occurs
DB_LOGGING=False

# Configure the redis connection credentials
REDIS_HOST="127.0.0.1"
REDIS_PORT=6379
REDIS_PASSWORD=""

REPORT_TABLE_NAME = "reports"
KEYWORD_BID_REPORT_TABLE_NAME = "keyword-bid-report"
AUTO_KEYWORD_REPORT_TABLE_NAME= "auto-keyword-report"
CAMPAIGN_PERFORMANCE_REPORT_TABLE_NAME = "campaign-performance-report"
DAILY_SKU_PERFORMANCE_REPORT_TABLE_NAME = "daily-sku-performance-report"
