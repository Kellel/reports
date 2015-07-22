import argparse
import sys
import os
import importlib

from parser import parser

parser.parse(sys.argv[1], sys.argv[2])

