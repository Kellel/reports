import sys

def usage():
    print "Usage: {} <num> < <filename>".format(sys.argv[0])
    print "Where <num> is the number of lines of the file you want"

try:
    lines = int(sys.argv[1])
except:
    usage()
    exit()
current = 1

for line in sys.stdin:

    for num, column in enumerate(line.split("\t"), start=1):
        print "{})\t{}".format(num, column)

    print "==============="

    current += 1
    if current > lines:
        break
