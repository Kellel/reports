import logging
import sys
import os
import imp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from redis import StrictRedis
from wrapper import ConfigurableWrapper

class Application(object):
    def __init__(self):
        self._done_config = False
        self._engine = None
        self._log = logging.getLogger('report-tool')
        self._session = ConfigurableWrapper(sessionmaker)
        self._redis = ConfigurableWrapper(StrictRedis)

    def setup(self, config_path=None):

        if not config_path:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_config.py')
        else:
            config_path = os.path.abspath(config_path)


        self.config = imp.load_source('report.config', config_path)

        self._log = logging.getLogger('report-tool')

        if hasattr(self.config, 'LOG_LEVEL'):
            self._log.setLevel(self.config.LOG_LEVEL.upper())
        else:
            self._log.setLevel(logging.INFO)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to log
        self._log.addHandler(ch)

        if hasattr(self.config, 'SQLALCHEMY_URI'):
            self._engine = create_engine(self.config.SQLALCHEMY_URI, echo=self.config.DB_LOGGING)
        else:
            self._engine = create_engine('sqlite:///test.db', echo=self.config.DB_LOGGING)

        self._session.setup(self.engine)

        self._redis.setup(host=self.config.REDIS_HOST, port=self.config.REDIS_PORT, password=self.config.REDIS_PASSWORD)

        self._done_config = True

    @property
    def engine(self):
        return self._engine

    @property
    def Session(self):
        return self._session

    @property
    def log(self):
        return self._log

    @property
    def redis(self):
        return self._redis

    @property
    def listen_key(self):
        if hasattr(self.config, 'REDIS_LISTEN_KEY'):
            return self.config.REDIS_LISTEN_KEY

        else:
            return "report-listen-queue"


    def create_db(self):
        from models import Base
        Base.metadata.create_all(self.engine)


application = Application()
Session = application.Session
engine = application.engine
log = application.log


## create log
#log = logging.getLogger('report-tool')
#log.setLevel(logging.INFO)
#
## create console handler and set level to debug
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#
## create formatter
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#
## add formatter to ch
#ch.setFormatter(formatter)
#
## add ch to log
#log.addHandler(ch)
#
#engine = create_engine('sqlite:///test.db', echo=False)
#Session = sessionmaker(bind=engine)
