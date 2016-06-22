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

class Backup(object):
    def __init__(self):
        self.sourceCache = None
        self.sourceReader = None
        self.sourceHasher = None
        
        self.sourcePath = None
        self.sourceCachePath = None
        self.label = None
    
    def setLabel(self, label):
        self.label = label    
        
    def setSourceCachePath(self, cachePath):
        self.sourceCachePath = cachePath
        
    def setSourcePath(self, path):
        self.sourcePath = path
        
    
        
    def initialize(self):
        self.sourceCache = sqlite.sqlite();
        self.sourceCache.setCacheLocation(self.sourceCachePath + ('DB-%s.sqlite' % (self.label)))

        self.sourceReader = LocalPathReaderCached.LocalPathReaderCached()
        self.sourceReader.setCache(self.sourceCache)
        self.sourceReader.setPath(self.sourcePath)
        self.sourceReader.initialize()

        self.sourceHasher = FastContentHashV1Cached.FastContentHashV1Cached()
        self.sourceHasher.setCache(self.sourceCache)
        self.sourceHasher.initialize()
        
    def destroy(self):
        self.sourceReader.destroy()
        self.sourceHasher.destroy()
        self.sourceCache.destroy()
    
    def scan(self):
        print "-"*80
        for p in iter(lambda:self.sourceReader.getNext(), None):
            print p.path
            if not p.isDir:
                print "    "+self.sourceHasher.hash(p)
        print "-"*80



src = Backup()
src.setLabel('x')
src.setSourcePath('/tmp/x/')
src.setSourceCachePath('/tmp/')
src.initialize()
src.scan()
src.destroy()