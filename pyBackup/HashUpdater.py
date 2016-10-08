# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
from Hasher.FullContentHashV1 import FullContentHashV1
from SourceReader.Path import Path
import Cache.sqlite as sqlite
from View.PathFormatter import PathFormatter
#import os
import math
import sys

"""
FIX: the backup analizer should use some coordinated sql's through the cache class (bases on sqlite3), not double-connecting to the sale DB
same for SimpleComparer
"""

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data',  dest='data', action='store', type=str,   default='',help='TODO')
parser.add_argument('--percent',  dest='percent', action='store', type=float,   default='',help='TODO')
parser.add_argument('--min',  dest='min', action='store', type=int,   default='',help='TODO')
args = vars(parser.parse_args())

pfmt = PathFormatter(120)

cache = sqlite.sqlite();
cache.setCacheLocation(args['cache'])
cache.initialize()

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

print "files with full hashes: %s files" % (analyzer.getFilesWithFullHashesCount())
print "files without full hashes: %s files" % (analyzer.getFilesWithoutFullHashesCount())

hh = FullContentHashV1.FullContentHashV1()
hh.initialize()

files = analyzer.getFilesWithoutFullHashes('random', 
    max(args['min'], math.ceil(analyzer.getFilesCount()*(args['percent']/100)))
)
sys.stdout.write("\n")
for (p, fhash, sz) in files:
    sys.stdout.write("\r    hash: %s" % (pfmt.format(p).ljust(120)))
    
    path = Path(p, False)
    path.size = sz
    
    hash = hh.hash(path)
    #print "    hash: %s" % (hash)
    cache.updateFileFullHashIntoFiles(path, hash)
cache.commit()

sys.stdout.write("\n")

hh.destroy()
analyzer.destroy()
cache.destroy()
