import os
import sys
import json

from redis import StrictRedis

redis = StrictRedis()

filename = sys.argv[1]

if os.path.isfile(filename):
    print "Sending File"
    msg = {
        'filename': sys.argv[1],
        'user': 'test'
    }
    redis.lpush('report-parser-queue', json.dumps(msg))

elif os.path.isdir(filename):
    print "Sending Directory"
    for root,directories, filenames in os.walk(filename):
        for filename in filenames:
            msg = {
                'filename': os.path.join(root,filename),
                'user': 'test'
            }
            redis.lpush('report-parser-queue', json.dumps(msg))
else:
    print "No such file or directory"


