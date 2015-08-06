# reports

Parse tab deliminated reports and enter them into a database.

## Install

1. clone this repo `git clone https://github.com/kellel/reports`
2. `cd reports`
3. python-pip is required
  * `apt-get install python-pip`
  * `yum install python-pip`
4. `python setup.py install`

## Running 

### report-daemon

The most basic usage requires nothing more than running the daemon as is

`report-daemon`

A better way to run the daemon would be to use something like supervisord

If you really must run the daemon from the command line maybe 

`report-daemon -f CONFIGFILE 2>&1 > /var/log/report-daemon.log &`

````
usage: report-daemon [-h] [-f FILE]

Run the report parser daemon

optional arguments:
  -h, --help              show this help message and exit
  -f FILE, --config FILE  Provide a config file
````

### report-cli
````
usage: report-cli [-h] {create,status} ...

cli for sending jobs to the report parser from the command line

positional arguments:
  {create,status}  sub-command help
    create         Create a job
    status         View the status the job queue

optional arguments:
  -h, --help       show this help message and exit
````

## Configuration
````
####                                                                              
#### REPORT DAEMON DEFAULT CONFIGURATION
####
 
# Database uri for more information lookup sqlalchemy database uri
SQLALCHEMY_URI="sqlite:///report.db"
#SQLALCHEMY_URI="mysql://user:pass@hostname:port/dbname"
#SQLALCHEMY_URI="postgresql+psycopg2://user:pass@hostname:port/dbname"

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
````
