# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
from os import listdir
from os.path import isdir, join, getatime, getmtime, getctime, getsize

import SourceReader.Path as Path
from SourceReader.LocalPathReader import LocalPathReader

class LocalPathReaderCached(LocalPathReader.LocalPathReader):
    def __init__(self):
        self.db = None
        super(LocalPathReaderCached, self).__init__()

    def setCache(self, cache):
        self.db = cache

    def initialize(self):
        print "LocalPathReaderCached.initialize %s" % (self.db.dbExists)
        if self.db.dbExists:
            self.paths = self.db.getAll()
        else:
            self.paths = self.goRecursivelly(self.basepath, [])
    
    def destroy(self):
        super(LocalPathReaderCached, self).destroy()
    
    def getNext(self):
        #print "LocalPathReaderCached.getNext %s" % (self.db.dbExists)
        
        if self.db.dbExists:
            ret = None
            if self.index<len(self.paths):
                p = self.paths[self.index]
                ret = Path.Path(None, None)
                ret.path = p[1]
                ret.isDir = bool(p[2])
                ret.ctime = int(p[3])
                ret.mtime = float(p[4])
                ret.size = int(p[5])
                self.index+=1
                
            if not self.progressCallback is None:
                self.progressCallback(self, 'getNext', {'p':ret})
                
            return ret
        else:
            ret = super(LocalPathReaderCached, self).getNext()
            if ret:
                self.db.insertFileIntoFiles(ret, '')
                if not self.progressCallback is None:
                    self.progressCallback(self, 'getNext', {'p':ret})
                
            return ret
            
