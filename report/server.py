#!/usr/bin/env python
import json
import argparse

from redis import StrictRedis

from parser import parser
from app import log, application

redis = StrictRedis()

class ReportParserServer(object):
    def __init__(self, listen_key):
        self._threads = []
        self._subscribed = False
        self.listen_key = listen_key
    def serve_forever(self):
        log.critical("SERVER STARTED listening on: %s", self.listen_key)
        try:
            while True:
                key, item = redis.brpop(self.listen_key)
                if key != self.listen_key:
                    print key
                    break
                self.work(item)
        except KeyboardInterrupt:
            pass

    def work(self, item):
        print "ITEM: " + str(item)
        message = json.loads(item)
        filename = message.get("filename")
        user = message.get("user")
        log.info("STARTING JOB FOR {}: {}".format(user, filename))
        parser.parse(filename, user)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the report parser daemon")
    parser.add_argument('-f', '--config', metavar='FILE', help="Provide a config file")
    args = parser.parse_args()
    application.setup(args.config)
    application.create_db()
    server = ReportParserServer('report-parser-queue')
    server.serve_forever()
