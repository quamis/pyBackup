# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os, time
from SimpleComparer import SimpleComparer

class CompleteComparer(SimpleComparer):
    def __init__(self):
        self.moved = None
    
    def initialize(self):
        super(CompleteComparer, self).initialize()
        self.moved = self.getAllMoved()
        
    def getAllMoved(self):
        if self.moved is None:
            self.moved = super(CompleteComparer, self).getAllMoved()
            
        return self.moved
    
    def getAllChanged(self):
        ret = super(CompleteComparer, self).getAllChanged()
        return self._filter(ret, [x[1] for x in self.moved])
    
    def getAllNew(self):
        ret = super(CompleteComparer, self).getAllNew()
        return self._filter(ret, [x[0] for x in self.moved])
    
    def getAllDeleted(self):
        ret = super(CompleteComparer, self).getAllDeleted()
        return self._filter(ret, [x[1] for x in self.moved])
    
    def _filter(self, list1, simplifiedList):
        temp3 = [x for x in list1 if x[0] not in simplifiedList]
        return temp3