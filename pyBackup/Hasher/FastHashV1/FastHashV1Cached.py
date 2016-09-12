# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import Hasher.Hasher as Hasher
from Hasher.FastHashV1 import FastHashV1

class FastHashV1Cached(FastHashV1.FastHashV1):
    def __init__(self):
        self.db = None
        super(FastHashV1Cached, self).__init__()
    
    def initialize(self):
        super(FastHashV1Cached, self).initialize()
    
    def destroy(self):
        super(FastHashV1Cached, self).destroy()
        
    def setCache(self, cache):
        self.db = cache
    
    def hash(self, path):
        h = self.db.findFileByPath(path.path)
        if h[0]:
            return h[0]
        else:
            h = super(FastHashV1Cached, self).hash(path)
            self.db.updateFileHashIntoFiles(path, h)
            return h