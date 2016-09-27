# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
from os import listdir
from os.path import isdir, join, getatime, getmtime, getatime, getctime, getsize, samefile

import SourceReader.Path as Path
from SourceReader.LocalPathReader import LocalPathReader

class LocalPathReaderCached(LocalPathReader.LocalPathReader):
    def __init__(self):
        self.cache = None
        self.useCache = True
        self.ignoredFiles = []
        super(LocalPathReaderCached, self).__init__()

    def setCache(self, cache):
        self.cache = cache
        
    def doUseCache(self, useCache):
        self.useCache = useCache>0

    def initialize(self):
        print "LocalPathReaderCached.initialize(). dbExists:%s, useCache:%s" % (self.cache.dbExists, self.useCache)
        if self.cache.dbExists and self.useCache:
            self.paths = self.cache.getAll()
        else:
            self.paths = self.goRecursivelly(self.basepath, [])
    
    def destroy(self):
        super(LocalPathReaderCached, self).destroy()
    
    def addIgnoredFile(self, p):
        self.ignoredFiles.append(p)
    
    def getNext(self):
        #print "LocalPathReaderCached.getNext %s" % (self.cache.dbExists)
        
        if self.cache.dbExists and self.useCache:
            ret = None
            if self.index<len(self.paths):
                p = self.paths[self.index]
                ret = Path.Path(None, None)

                if self._isIgnored(p[1]):
                    return self.getNext()
                
                ret.path = p[1]
                ret.isDir = bool(p[2])
                ret.ctime = int(p[3])
                ret.mtime = float(p[4])
                ret.atime = float(p[5])
                ret.size = int(p[6])
                self.index+=1
                
            if not self.progressCallback is None:
                self.progressCallback(self, 'getNext', {'p':ret})
                
            return ret
        else:
            ret = super(LocalPathReaderCached, self).getNext()

            if ret:
                if self._isIgnored(ret.path):
                    return self.getNext()
                
                self.cache.insertFileIntoFiles(ret, '')
                if not self.progressCallback is None:
                    self.progressCallback(self, 'getNext', {'p':ret})
                
            return ret
            
            
            
    def _isIgnored(self, path):
        for p in self.ignoredFiles:
            if samefile(path, p):
                return True
            
        return False
