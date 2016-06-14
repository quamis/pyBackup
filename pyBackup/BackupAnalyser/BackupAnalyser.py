# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os, time

class BackupAnalyser(object):
    def __init__(self):
        self.cacheOld = None
        self.cacheNew = None
        self.conn = None
        
    def setCache(self, cache):
        self.cacheNew = cache

    def initialize(self):
        self.conn = sqlite3.connect(self.cacheNew.db)
        c = self.conn.cursor()
    
    def destroy(self):
        self.conn.commit()
        self.conn.close()
        
    def getTotalCount(self):
        pass
        
    def getTotalSize(self):
        pass
        
    def getAvgSize(self):
        pass
        
    def getDuplicatedFilesCount(self):
        pass
        
    def getDuplicatedFilesSize(self):
        pass
        
    def getEmptyFilesCount(self):
        pass