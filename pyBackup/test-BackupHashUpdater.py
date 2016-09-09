# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import pprint
import humanize
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
import Cache.sqlite as sqlite
import os
import math

pp = pprint.PrettyPrinter(indent=4)

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data',  dest='data', action='store', type=str,   default='',help='TODO')
parser.add_argument('--percent',  dest='percent', action='store', type=float,   default='',help='TODO')
args = vars(parser.parse_args())


cache = sqlite.sqlite();
cache.setCacheLocation(args['cache'])

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

#TODO: number of files per type (music/jpg/others)
#TODO: size of files per type (music/jpg/others)

print "files with full hashes: %s files" % (analyzer.getFilesWithFullHashesCount())
print "files without full hashes: %s files" % (analyzer.getFilesWithoutFullHashesCount())

for (path, hash) in analyzer.getFilesWithoutFullHashes('random', math.ceil(analyzer.getFilesWithoutFullHashesCount()*(args['percent']/100))):
    print "check file %s" % (path)

analyzer.destroy()


