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
import logging

"""
FIX: the backup analizer should use some coordinated sql's through the cache class (bases on sqlite3), not double-connecting to the sale DB
same for SimpleComparer
"""

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data',  dest='data', action='store', type=str,   default='',help='TODO')
parser.add_argument('--percent',  dest='percent', action='store', type=float,   default='',help='TODO')
parser.add_argument('--min',  dest='min', action='store', type=int,   default='',help='TODO')
parser.add_argument('--verbose',  dest='verbose', action='store', type=int,   default='',help='TODO')
args = vars(parser.parse_args())

if args['verbose']>=4:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%Y%m%d %I:%M:%S')
else:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.WARNING, datefmt='%Y%m%d %I:%M:%S')

pfmt = PathFormatter(120)

cache = sqlite.sqlite();
cache.setCacheLocation(args['cache'])
cache.initialize()

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

logging.info("files with full hashes: %s files" % (analyzer.getFilesWithFullHashesCount()))
logging.info("files without full hashes: %s files" % (analyzer.getFilesWithoutFullHashesCount()))

hh = FullContentHashV1.FullContentHashV1()
hh.initialize()

files = analyzer.getFilesWithoutFullHashes('random', 
    max(args['min'], math.ceil(analyzer.getFilesCount()*(args['percent']/100)))
)
for (p, fhash, sz) in files:
    logging.info("    hash: %s" % (pfmt.format(p).ljust(120)))
    
    path = Path(p, False)
    path.size = sz
    
    hash = hh.hash(path)
    #print "    hash: %s" % (hash)
    cache.updateFileFullHashIntoFiles(path, hash)
cache.commit()

hh.destroy()
analyzer.destroy()
cache.destroy()
