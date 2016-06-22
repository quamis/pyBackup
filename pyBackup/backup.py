# -*- coding: utf-8 -*-
'''
@author: lucian
'''

"""
 - scan the "source" folder
 - scan the "target" folder (this should mean to basically load & initialize the cache file
 - compute diffs
 - apply diffs
 - display some stats
 
run as 
    python ./backup.py
"""

from SourceReader.LocalPathReader import LocalPathReaderCached
from SourceReader.LocalPathReader import LocalPathReader
from Hasher.FastContentHashV1 import FastContentHashV1
from Hasher.FastContentHashV1 import FastContentHashV1Cached
import Cache.sqlite as sqlite

class Source(object):
    def __init__(self):
        self.cache = None
        self.reader = None
        self.hasher = None
        
        self.path = None
        self.cachePath = None
        self.label = None
        
        
    def setCachePath(self, cachePath):
        self.cachePath = cachePath
        
    def setPath(self, path):
        self.path = path
        
    def setLabel(self, label):
        self.label = label
        
    def initialize(self):
        self.cache = sqlite.sqlite();
        self.cache.setCacheLocation(self.cachePath + ('DB-%s.sqlite' % (self.label)))

        self.reader = LocalPathReaderCached.LocalPathReaderCached()
        self.reader.setCache(self.cache)
        self.reader.setPath(self.path)
        self.reader.initialize()

        self.hasher = FastContentHashV1Cached.FastContentHashV1Cached()
        self.hasher.setCache(self.cache)
        self.hasher.initialize()
        
    def destroy(self):
        self.reader.destroy()
        self.hasher.destroy()
        self.cache.destroy()
    
    def scan(self):
        print "-"*80
        for p in iter(lambda:self.reader.getNext(), None):
            print p.path
            if not p.isDir:
                print "    "+self.hasher.hash(p)
        print "-"*80



src = Source()
src.setPath('/tmp/x/')
src.setCachePath('/tmp/')
src.setLabel('source,x,001')
src.initialize()
src.scan()
src.destroy()