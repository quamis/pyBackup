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
import logging
import sys

def retry_calls(fcn, onError):
    errorCnt = 0
    while True:
        try:
            fcn()
            break
        except (IOError, OSError) as e:
            errorCnt+=1
            if onError(errorCnt, fcn):
                logging.error("retried %s times. Error: %s" % (errorCnt, e.strerror))
                raise e

def onError_default(errorCnt, fcn):
    time.sleep(0.5*errorCnt)
    print("retry %d: %s" % (errorCnt, inspect.getsource(fcn).strip()))
    if errorCnt>5:
        return True
    return False
    

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
parser.add_argument('--stopOnFirstFail',dest='stopOnFirstFail', action='store', type=int,   default=1, help='TODO')
parser.add_argument('--verbose',        dest='verbose',         action='store', type=int,   default='',help='TODO')
args = vars(parser.parse_args())

if args['verbose']>=4:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%Y%m%d %I:%M:%S')
elif args['verbose']>=2:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.WARNING, datefmt='%Y%m%d %I:%M:%S')
elif args['verbose']>=1:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.ERROR, datefmt='%Y%m%d %I:%M:%S')
else:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.ERROR, datefmt='%Y%m%d %I:%M:%S')

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


failedChecks = []
for (np, fhash, sz, fullHash) in files:
    op = wrt.getDestinationFilePath(np)
        
    logging.info("    check: %s" % (pfmt.format(op).ljust(120)))
    path = Path(wrt.getDestinationFilePathToContent(op), False)
    path.size = sz
    
    hash = hh.hash(path)
    if hash!=fullHash:
        failedChecks.append({
            'np':       np, 
            'hash':     hash, 
            'fullHash': fullHash,
        })
        
        if args['stopOnFirstFail']:
            logging.error("!"*80)
            logging.error("!   fullHash check failed!")
            logging.error("!   path: %s" % (np))
            logging.error("!   fullHash: %s" % (hash))
            logging.error("!   expected: %s" % (fullHash))
            logging.error("!"*80)
            sys.exit(1)
        else:
            logging.error("       fullHash check failed, continuing")

retry_calls( lambda: cache.commit(), onError_default)


if len(failedChecks):
    logging.error("\n\n")
    logging.error("!"*80)
    
    logging.error("!   fullHash check failed!")
    for o in failedChecks:
        logging.error("!   path: %s" % (o['np']))
        logging.error("!   fullHash: %s" % (o['hash']))
        logging.error("!   expected: %s\n\n" % (o['fullHash']))
    
    logging.error("")
    logging.error("")
    logging.error("found %d failed files, out of %d" % (len(failedChecks), len(files)))
        
    logging.error("!"*80)

    if args['verbose']==1:
        for o in failedChecks:
            print("%s" % (o['np']))
    sys.exit(1)
else:
    logging.info("check done, all good")

hh.destroy()
analyzer.destroy()
cache.destroy()
wrt.destroy()
