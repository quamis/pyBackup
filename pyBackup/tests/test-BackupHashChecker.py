# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import humanize
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
from Hasher.FullContentHashV1 import FullContentHashV1
from Writer.LocalPathWriter.Writer import Writer
from SourceReader.Path import Path
import Cache.sqlite as sqlite
from View.PathFormatter import PathFormatter
#import os
import math
import sys
import logging

"""
FIX: the backup analizer should use some coordinated sql's through the cache class (bases on sqlite3), not double-connecting to the sale DB
same for SimpleComparer
"""
parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cacheOld',       dest='cacheOld',        action='store', type=str,   default='',help='TODO')
parser.add_argument('--source',         dest='source',          action='store', type=str,   default='',help='TODO')
parser.add_argument('--destination',    dest='destination',     action='store', type=str,   default='',help='TODO')
parser.add_argument('--percent',        dest='percent',         action='store', type=float, default='',help='TODO')
parser.add_argument('--min',            dest='min',             action='store', type=int,   default='',help='TODO')
args = vars(parser.parse_args())

pfmt = PathFormatter(120)

cache = sqlite.sqlite();
cache.setCacheLocation(args['cacheOld'])
cache.initialize()

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

logging.info("files with full hashes: %s files" % (analyzer.getFilesWithFullHashesCount()))

hh = FullContentHashV1.FullContentHashV1()
hh.initialize()

wrt = Writer(args['destination'], args['source'])
wrt.initialize()

files = analyzer.getFilesWithFullHashes('random', 
    max(args['min'], math.ceil(analyzer.getFilesWithFullHashesCount()*(args['percent']/100)))
)

sys.stdout.write("\n")
for (np, fhash, sz, fullHash) in files:
    op = wrt.getDestinationFilePath(np)
        
    sys.stdout.write("\r    check: %s" % (pfmt.format(op).ljust(120)))
    path = Path(wrt.getDestinationFilePathToContent(op), False)
    path.size = sz
    
    hash = hh.hash(path)
    if hash!=fullHash:
        logging.error("!"*80)
        logging.error("!   fullHash check failed!")
        logging.error("!   fullHash: %s, expected: %s" % (hash, fullHash))
        logging.error("!"*80)


cache.commit()

hh.destroy()
analyzer.destroy()
cache.destroy()
wrt.destroy()