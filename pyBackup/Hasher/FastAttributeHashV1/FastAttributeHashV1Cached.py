# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
#import Hasher.Hasher as Hasher
from Hasher.FastAttributeHashV1 import FastAttributeHashV1

class FastAttributeHashV1Cached(FastAttributeHashV1.FastAttributeHashV1):
    def __init__(self):
        self.cache = None
        super(FastAttributeHashV1Cached, self).__init__()
    
    def initialize(self):
        super(FastAttributeHashV1Cached, self).initialize()
    
    def destroy(self):
        super(FastAttributeHashV1Cached, self).destroy()
        
    def setCache(self, cache):
        self.cache = cache
    
    def hash(self, path):
        h = self.cache.findFileByPath(path.path)
        if h[0]:
            return h[0]
        else:
            h = super(FastAttributeHashV1Cached, self).hash(path)
            self.cache.updateFileHashIntoFiles(path, h)
            return h
        