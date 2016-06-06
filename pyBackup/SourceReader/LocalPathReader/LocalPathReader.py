# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
from os import listdir
from os.path import isdir, join

import SourceReader.Path as Path 

class LocalPathReader():
    def __init__(self):
        self.index = 0;
        pass

    def setPath(self, basepath):
        self.basepath = basepath

    def initialize(self):
        self.paths = self.goRecursivelly(self.basepath, [])


    def goRecursivelly(self, basepath, paths):
        for p in listdir(basepath):
            fp = join(basepath, p)
            isDir = isdir(fp)
            np = Path.Path(fp, isDir)
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
