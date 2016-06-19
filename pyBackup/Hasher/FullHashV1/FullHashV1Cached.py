# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import Hasher.Hasher as Hasher
from Hasher.FullHashV1 import FullHashV1

class FullHashV1Cached(FullHashV1.FullHashV1):
    def __init__(self):
        self.db = None
        super(FullHashV1Cached, self).__init__()
    
    def initialize(self):
        self.db.initialize()
        super(FullHashV1Cached, self).initialize()
    
    def destroy(self):
        self.db.destroy()
        super(FullHashV1Cached, self).initialize()
        
    def setCache(self, cache):
        self.db = cache
    
    def hash(self, path):
        h = self.db.findFileByPath(path.path)
        if h[0]:
            return h[0]
        else:
            h = super(FullHashV1Cached, self).hash(path)
            self.db.updateFileHashIntoFiles(path, h)
            return h
        