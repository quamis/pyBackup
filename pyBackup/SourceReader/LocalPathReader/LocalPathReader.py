# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
from os import listdir
from os.path import isdir, join, getatime, getmtime, getctime, getsize

import SourceReader.Path as Path 

class LocalPathReader(object):
    def __init__(self):
        self.index = 0;
        self.paths = []
        self.progressCallback = None

    def setPath(self, basepath):
        self.basepath = basepath

    def initialize(self):
        self.paths = self.goRecursivelly(self.basepath, [])
    
    def destroy(self):
        self.paths = []
        
    def registerProgressCallback(self, callback):
        self.progressCallback = callback
        
    def goRecursivelly(self, basepath, paths):
        for p in listdir(unicode(basepath)):
            fp = unicode(join(basepath, p))
            isDir = isdir(fp)
            np = Path.Path(fp, isDir)
            np.ctime = getctime(fp)
            np.mtime = getmtime(fp)
            np.size = getsize(fp)
            
            if not self.progressCallback is None:
                self.progressCallback(self, 'newPath', {'p':np, 'isDir':isDir})
            
            paths.append(np)

            if isDir:
                paths = self.goRecursivelly(fp, paths)

        return paths

    def getNext(self):
        ret = None
        if self.index<len(self.paths):
            ret = self.paths[self.index]
            self.index+=1
        return ret
