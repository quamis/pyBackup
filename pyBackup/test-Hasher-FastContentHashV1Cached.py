# -*- coding: utf-8 -*-
'''
@author: lucian
'''

"""
run as 
    rm ./FileSystem.sqlite; python ./test-Hasher-FastContentHashV1Cached.py
"""
import argparse
from SourceReader.LocalPathReader import LocalPathReaderCached
from SourceReader.LocalPathReader import LocalPathReader
from Hasher.FastContentHashV1 import FastContentHashV1
from Hasher.FastContentHashV1 import FastContentHashV1Cached

from Hasher.FastContentHashV2 import FastContentHashV2Cached

import Cache.sqlite as sqlite

from View.PathFormatter import PathFormatter

import sys
import os, time


def callbackLocalPathReader(lp, event, data):
    global stats
    tm = time.time()
    
    evtps = "[ ....e/s]"
    if not stats['isWarmingUp']:
        evtps = "[%5.1fe/s]" % (stats['evtps'])
    
    if event=='newPath':
        stats[event] = stats[event]+1
        if not data['isDir']:
            sys.stdout.write("\r %s new : %50s" % (evtps, pfmt.format(data['p'].path).ljust(120)))
            
    if event=='getNext':
        stats[event] = stats[event]+1
        if not data['p'].isDir:
            sys.stdout.write("\r %s next: %50s" % (evtps, pfmt.format(data['p'].path).ljust(120)))
    
        if stats['getNext']>20 and tm - stats['resetTime'] > 2.5:
            stats['evtps'] = (stats['getNext']) / (tm - stats['startTime'])
            stats['isWarmingUp'] = False
        
    if tm - stats['resetTime'] > 30:
        stats = {
            'startTime':tm,
            'resetTime':tm, 
            'newPath':0, 
            'getNext':0, 
            'evtps':stats['evtps']/10,
            'isWarmingUp':True, 
        }
    #sys.stdout.flush()
    
parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data', 	dest='data',   action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose', dest='verbose',   action='store', type=int,   default=1,help='TODO')
parser.add_argument('--useCache', dest='useCache',   action='store', type=int,   default=1, help='TODO')
args = vars(parser.parse_args())

pfmt = PathFormatter(120)
stime = time.time()
stats = {
    'startTime':time.time(), 
    'resetTime':time.time(), 
    'newPath':0, 
    'getNext':0, 
    'evtps':0.0, 
    'isWarmingUp':True, 
}


cache = sqlite.sqlite();

lp = LocalPathReaderCached.LocalPathReaderCached()
lp.setCache(cache)
#lp = LocalPathReader.LocalPathReader()

cache.setCacheLocation(args['cache'])
cache.initialize()

cache.resetFilesData()

lp.doUseCache(args['useCache'])
lp.setPath(args['data'])

if cache.getFlag('app.run.first') is None:
    cache.setFlag('app.run.count', 0)
    cache.setFlag('app.run.first', time.time())
    cache.setFlag('cache.path', args['cache'])
    cache.setFlag('data.path', args['data'])

cache.setFlag('app.run.last', time.time())
cache.setFlag('app.run.count', int(cache.getFlag('app.run.count'))+1)

cache.log("[%s] start" % (os.path.basename(__file__)))



lp.registerProgressCallback(callbackLocalPathReader)
lp.initialize()

lp.addIgnoredFile(args['cache'])
lp.addIgnoredFile(args['cache']+"-journal")

#hh = FastContentHashV1Cached.FastContentHashV1Cached()
hh = FastContentHashV2Cached.FastContentHashV2Cached()
hh.setCache(cache)
hh.initialize()

if args['verbose']>0:
    print "-"*80
    for p in iter(lambda:lp.getNext(), None):
        print p.path
        if not p.isDir:
            print "    "+hh.hash(p)
    print "-"*80
else:
    for p in iter(lambda:lp.getNext(), None):
        if not p.isDir:
            hh.hash(p)
    
    
lp.destroy()
hh.destroy()

cache.log("[%s] done" % (os.path.basename(__file__)))

cache.commit()
cache.destroy()

print ""
