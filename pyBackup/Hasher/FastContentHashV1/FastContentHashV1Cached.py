# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
#import Hasher.Hasher as Hasher
#from FastContentHashV1 import FastContentHashV1
from Hasher.FastContentHashV1 import FastContentHashV1

class FastContentHashV1Cached(FastContentHashV1.FastContentHashV1):
    def __init__(self):
        self.cache = None
        super(FastContentHashV1Cached, self).__init__()
    
    def initialize(self):
        super(FastContentHashV1Cached, self).initialize()
    
    def destroy(self):
        super(FastContentHashV1Cached, self).destroy()
        
    def setCache(self, cache):
        self.cache = cache
    
    def hash(self, path):
        h = self.cache.findFileByPath(path.path)
        if h[0]:
            return h[0]
        else:
            h = super(FastContentHashV1Cached, self).hash(path)
            self.cache.updateFileHashIntoFiles(path, h)
            return h
        