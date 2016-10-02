# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
class mangledPath(object):
    def __init__(self, cache):
        self.cache = cache
        
    def __getattr__(self, attr):
        if attr=="initialize":
            self.cache._pathCleanup = self._pathCleanup
            
        return getattr(self.cache, attr)
    
    def _pathCleanup(self, p):
        raise RuntimeError("Implement & overwrite this function!!")
        