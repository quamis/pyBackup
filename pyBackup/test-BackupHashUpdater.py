# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import pprint
import humanize
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
from Hasher.FullContentHashV1 import FullContentHashV1
from SourceReader.Path import Path
import Cache.sqlite as sqlite
#import os
import math

"""
FIX: the backup analizer should use some coordinated sql's through the cache class (bases on sqlite3), not double-connecting to the sale DB
same for SimpleComparer
"""

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data',  dest='data', action='store', type=str,   default='',help='TODO')
parser.add_argument('--percent',  dest='percent', action='store', type=float,   default='',help='TODO')
args = vars(parser.parse_args())


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
        min(100, math.ceil(analyzer.getFilesWithoutFullHashesCount()*(args['percent']/100)))
    )
#files = analyzer.getFilesWithoutFullHashes('random', 1)
for (p, hash, sz) in files:
    print "check file %s" % (p)
    path = Path(p, False)
    path.size = sz
    
    hash = hh.hash(path)
    print "    hash: %s" % (hash)
    cache.updateFileFullHashIntoFiles(path, hash)
cache.commit()

hh.destroy()
analyzer.destroy()
cache.destroy()





