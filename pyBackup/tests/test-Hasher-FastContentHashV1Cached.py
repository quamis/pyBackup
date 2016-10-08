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
from View.ScriptStatusTracker import ScriptStatusTracker
import sys
import os, time
import logging

class LogTracker(ScriptStatusTracker):
    def storeEvent(self, tm, event, data):
        k = "size:"+event
        if not k in self.totalEvents:
            self.totalEvents[k] = 0
        
        self.totalEvents[k]+= data['p'].size
        return super(LogTracker, self).storeEvent(tm, event, data)
        
    def composeOutputStr(self, statusStr, tm, event, data):
        mbps = "---.-Mb/s"
        if event=='getNext' and self.totalEvents["getNext"]>10:
            v = float(self.totalEvents["size:getNext"])/(tm - self.stats['startTime'])/(1024*1024)
            mbps = "%5.1fMb/s" % (min(v, 999.9))
            
        return "%s%s %8s: %s" % (statusStr, mbps, event, self.pfmt.format(data['p'].path).ljust(120))
        
    def calcStats(self, tm):
        if 'getNext' in self.events and self.events['getNext']>10 and tm - self.stats['resetTime'] > 1.0:
            avg = (self.events['getNext']) / (tm - self.stats['resetTime'])
            
            self.stats['evtps'] = avg
            self.stats['isWarmingUp'] = False
        elif 'newPath' in self.events and self.events['newPath']>10 and tm - self.stats['resetTime'] > 1.0:
            avg = (self.events['newPath']) / (tm - self.stats['resetTime'])
            self.stats['evtps'] = avg
            self.stats['isWarmingUp'] = False
            
        if 'newPath' in self.totalEvents and 'getNext' in self.totalEvents and self.stats['expectedEvents'] is None:
            self.stats['expectedEvents'] = self.totalEvents['newPath']
            self.resetStats(tm)
            
        if not self.stats['expectedEvents'] is None:
            self.stats['evtpg'] = self.totalEvents['getNext']/float(self.stats['expectedEvents'])

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

if args['verbose']>=4:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%Y%m%d %I:%M:%S')
else:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.WARNING, datefmt='%Y%m%d %I:%M:%S')

tracker = LogTracker(args['verbose'])



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

for p in iter(lambda:lp.getNext(), None):
    if not p.isDir:
        logging.info("    hash: %s" % (hh.hash(p)))
    
lp.destroy()
hh.destroy()

cache.log("[%s] done" % (os.path.basename(__file__)))

cache.commit()
cache.destroy()
