# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os, time

class BackupAnalyzer(object):
    def __init__(self):
        self.cache = None
        self.conn = None
        
    def setCache(self, cache):
        self.cache = cache

    def initialize(self):
        self.conn = sqlite3.connect(self.cache.db)
        c = self.conn.cursor()
    
    def destroy(self):
        self.conn.commit()
        self.conn.close()
        
    def getTotalCount(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM main.files AS fn WHERE NOT fn.isDir')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getTotalSize(self):
        c = self.conn.cursor()
        c.execute('SELECT SUM(size) FROM main.files AS fn WHERE NOT fn.isDir')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getAvgSize(self):
        c = self.conn.cursor()
        c.execute('SELECT SUM(size)/COUNT(*) FROM main.files AS fn WHERE NOT fn.isDir')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getMedianSize(self):
        c = self.conn.cursor()
        #c.execute('SELECT MEDIAN(size) FROM main.files AS fn WHERE NOT fn.isDir')
        # @see http://stackoverflow.com/a/15766121/11301
        c.execute('''
            SELECT AVG(size) FROM (
                SELECT size FROM main.files 
                WHERE NOT isDir
                ORDER BY size DESC
                LIMIT 2 - ((SELECT COUNT(*) FROM main.files WHERE NOT isDir) % 2)    -- odd 1, even 2
                OFFSET (SELECT (COUNT(*) - 1) / 2 FROM main.files WHERE NOT isDir)
             )''')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getDuplicatedFilesCount(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) AS cnt FROM main.files AS fn WHERE NOT fn.isDir GROUP BY fn.hash HAVING cnt>1')
        return sum(((cnt-1) for (cnt, ) in c.fetchall() if True))
        
    def getDuplicatedFilesSize(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) AS cnt, size FROM main.files AS fn WHERE NOT fn.isDir GROUP BY fn.hash HAVING cnt>1')
        return sum(((size*(cnt-1)) for (cnt, size) in c.fetchall() if True))
        
    def getEmptyFilesCount(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) AS cnt FROM main.files AS fn WHERE NOT fn.isDir AND size=0 GROUP BY fn.hash')
        r = c.fetchone()
        return 0 if r is None else r[0]
    
    def getTop10LargestFiles(self):
        c = self.conn.cursor()
        c.execute('SELECT fn.size, fn.path FROM main.files AS fn WHERE NOT fn.isDir ORDER BY fn.size DESC LIMIT 10')
        return c.fetchall()
    
    