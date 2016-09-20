# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os, time
from SimpleComparer import SimpleComparer

class CompleteComparer(SimpleComparer):
    def __init__(self):
        self.moved = None
    
    def initialize(self):
        super(CompleteComparer, self).initialize()
        self.moved = self.getMovedFiles()
        
    def getMovedFiles(self):
        if self.moved is None:
            self.moved = super(CompleteComparer, self).getMovedFiles()
            
        return self.moved
    
    def getChangedFiles(self):
        ret = super(CompleteComparer, self).getChangedFiles()
        return self._filter(ret, [x[1] for x in self.moved])
    
    def getNewFiles(self):
        ret = super(CompleteComparer, self).getNewFiles()
        return self._filter(ret, [x[0] for x in self.moved])
    
    def getDeletedFiles(self):
        ret = super(CompleteComparer, self).getDeletedFiles()
        return self._filter(ret, [x[1] for x in self.moved])
    
    def _filter(self, list1, simplifiedList):
        temp3 = [x for x in list1 if x[0] not in simplifiedList]
        return temp3