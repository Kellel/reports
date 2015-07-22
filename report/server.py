#!/usr/bin/env python
import json
import argparse

from parser import parser, ParseError
from app import log, application

class ReportParserServer(object):
    def __init__(self, listen_key):
        self._threads = []
        self._subscribed = False
        self.listen_key = listen_key
        self.redis = application.redis
    def serve_forever(self):
        log.critical("SERVER STARTED listening on: %s", self.listen_key)
        try:
            while True:
                key, item = self.redis.brpop(self.listen_key)
                if key != self.listen_key:
                    print key
                    break
                self.work(item)
        except KeyboardInterrupt:
            pass

    def work(self, item):
        try:
            message = json.loads(item)
        except ValueError:
            log.exception("Message parsing failed")
            return

        filename = message.get("filename")
        user = message.get("user")
        log.info("STARTING JOB FOR {}: {}".format(user, filename))

        try:
            parser.parse(filename, user)
        except ParseError:
            log.exception("Parsing Error")
        except IOError:
            log.exception("Error opening file")
        except:
            log.exception("An unknown error has occured")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the report parser daemon")
    parser.add_argument('-f', '--config', metavar='FILE', help="Provide a config file")
    args = parser.parse_args()
    application.setup(args.config)
    application.create_db()
    server = ReportParserServer('report-parser-queue')
    server.serve_forever()
