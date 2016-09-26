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

class LogTracker(object):
    def __init__(self):
        self.pfmt = PathFormatter(120)
        t = time.time()
        self.stats = {
            'startTime':    t,
            'resetTime':    t,
            'flushTime':    t,
            'evtps':        0.0, 
            'totalEvents': 0,
            'isWarmingUp':True, 
        }
        
        self.events = {}
        self.totalEvents = {}

    
    def storeEvent(self, tm, event, data):
        if not event in self.events:
            self.events[event] = 0
        self.events[event]+= 1
        
        if not event in self.totalEvents:
            self.totalEvents[event] = 0
        self.totalEvents[event]+= 1
        
        self.stats['totalEvents']+= 1
        
    def resetStats(self, tm):
        if tm - self.stats['resetTime'] > 30:
            self.stats['resetTime'] =    tm
            #stats['evtps'] =        0
            self.stats['isWarmingUp'] =  True
            
            self.events =           {}
            
        
    def calcStats(self, tm):
        if 'getNext' in self.events and self.events['getNext']>10 and tm - self.stats['resetTime'] > 1.0:
            avg = (self.events['getNext']) / (tm - self.stats['resetTime'])
            
            self.stats['evtps'] = avg
            self.stats['isWarmingUp'] = False
    
    def logEvent(self, tm, event, data):
        evtps = "[ ....e/s]"
        if not self.stats['isWarmingUp']:
            evtps = "[%5.1fe/s]" % (self.stats['evtps'])
            
        pgpc = "[....%]"
        if 'newPath' in self.totalEvents and 'getNext' in self.totalEvents:
            pgpc = "[%4.1f%%]" % (99.9*self.totalEvents['getNext']/self.totalEvents['newPath'])

        if event=='newPath':
            sys.stdout.write("\r %s%s new : %50s" % (pgpc, evtps, self.pfmt.format(data['p'].path).ljust(120)))
            
        if event=='getNext':
            if not data['p'].isDir:
                sys.stdout.write("\r %s%s next: %50s" % (pgpc, evtps, self.pfmt.format(data['p'].path).ljust(120)))
                
        self.calcStats(tm)
        self.resetStats(tm)
            
        if tm - self.stats['flushTime'] > 1:
            self.stats['flushTime'] = tm
            sys.stdout.flush()

def callbackLocalPathReader(lp, event, data):
    tm = time.time()
    tracker.storeEvent(tm, event, data)
    tracker.logEvent(tm, event, data)
    
    
parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data', 	dest='data',   action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose', dest='verbose',   action='store', type=int,   default=1,help='TODO')
parser.add_argument('--useCache', dest='useCache',   action='store', type=int,   default=1, help='TODO')
args = vars(parser.parse_args())

tracker = LogTracker()



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
