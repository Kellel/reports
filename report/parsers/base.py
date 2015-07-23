import re
import os

from ..models import Report
from ..app import log, application

class ParseError(Exception):
    """
    These are raised when there is an error in the input file
    """
    pass

class BasicParser(object):
    FIRST_REGEX = "^.*$"
    LINE_REGEX = "^.*$"

    def __init__(self):
        log.debug("COMPILING %s", self.FIRST_REGEX)
        self._first_regex = re.compile(self.FIRST_REGEX)
        log.debug("COMPILING %s", self.LINE_REGEX)
        self._line_regex = re.compile(self.LINE_REGEX)
        self._session = None
        self._con = None
        self._insert_queue = []
        self.max_pending_rows = 100

    @property
    def session(self):
        if not self._session:
            self._session = application.Session()
        return self._session

    @property
    def connection(self):
        if not self._con:
            self._con = application.engine.connect()
        return self._con

    def cleanup(self):
        self.session.commit()
        self.session.close()

    def parse(self, fqn, user, catch_errors):
        """
        Take a filepath and split process it line by line
        """

        self.filename = fqn
        self.user = user


        print "&##&#&#&# THIS TIS SD:LFKJ SD:LKFJ KLSDJFL :KJFL:K J##################"


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

        self.flush()
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

    def insert_dict(self, dictionary):
        """
        Put an object into our insert list for a pending insert
        """
        log.debug("Added item to data queue")
        self._insert_queue.append(dictionary)
        if len(self._insert_queue) > self.max_pending_rows:
            self.flush()

    def flush(self):
        log.info("COMMITING DATA")
        self.connection.execute(self.DB_CLS.__table__.insert(), list(self._insert_queue))
        self._insert_queue = []
