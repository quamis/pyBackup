# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os, time

class BackupAnalyzer(object):
    def __init__(self):
        self.cache = None
        
    def setCache(self, cache):
        self.cache = cache

    def initialize(self):
        pass
    
    def destroy(self):
        self.cache.commit()
        
    def getFilesCount(self):
        c = self.cache.cursor()
        c.execute('SELECT COUNT(*) FROM main.files AS fn WHERE NOT fn.isDir')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getFilesWithFullHashesCount(self):
        c = self.cache.cursor()
        c.execute('SELECT COUNT(*) FROM main.files AS fn WHERE NOT fn.isDir AND fn.fullHash!=""')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getFilesWithoutFullHashesCount(self):
        c = self.cache.cursor()
        c.execute('SELECT COUNT(*) FROM main.files AS fn WHERE NOT fn.isDir AND NOT fn.fullHash=""')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getFilesWithoutFullHashes(self, order, limit):
        c = self.cache.cursor()
        if order=='random':
            val = (limit, )
            c.execute('SELECT fn.path, fn.hash, fn.size FROM main.files AS fn WHERE NOT fn.isDir AND fn.fullHash="" ORDER BY RANDOM() LIMIT ?', val)
        else:
            raise RuntimeError("Invalid order param")
            
        r = c.fetchall()
        return r
        
    def getDirsCount(self):
        c = self.cache.cursor()
        c.execute('SELECT COUNT(*) FROM main.files AS fn WHERE fn.isDir')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getEmptyDirsCount(self):
        # TODO
        c = self.cache.cursor()
        c.execute('''
            SELECT COUNT(*) FROM main.files AS f1 WHERE 
                f1.isDir 
                AND f1.path NOT IN (
                    SELECT f2.path FROM main.files AS f2 WHERE 
                        f2.isDir 
                        AND (
                            SELECT 1 FROM main.files AS f3 WHERE 
                                NOT f3.isDir 
                                AND f3.path LIKE f2.path || "%" LIMIT 1
                            )
                )''')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
        
    def getTotalSize(self):
        c = self.cache.cursor()
        c.execute('SELECT SUM(size) FROM main.files AS fn WHERE NOT fn.isDir')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getSizeByExtensionList(self, list):
        c = self.cache.cursor()
        query = '''SELECT SUM(size) FROM main.files AS fn WHERE 
            NOT fn.isDir 
            AND (
                LOWER(SUBSTR(fn.path, -2)) IN ('%s')
                OR LOWER(SUBSTR(fn.path, -3)) IN ('%s')
                OR LOWER(SUBSTR(fn.path, -4)) IN ('%s')
                OR LOWER(SUBSTR(fn.path, -5)) IN ('%s')
                OR LOWER(SUBSTR(fn.path, -6)) IN ('%s')
                OR LOWER(SUBSTR(fn.path, -7)) IN ('%s')
                OR LOWER(SUBSTR(fn.path, -8)) IN ('%s')
                OR LOWER(SUBSTR(fn.path, -9)) IN ('%s')
            )
            ''' % (
            "', '".join(sorted([x for x in list if len(x)==2])),
            "', '".join(sorted([x for x in list if len(x)==3])),
            "', '".join(sorted([x for x in list if len(x)==4])),
            "', '".join(sorted([x for x in list if len(x)==5])),
            "', '".join(sorted([x for x in list if len(x)==6])),
            "', '".join(sorted([x for x in list if len(x)==7])),
            "', '".join(sorted([x for x in list if len(x)==8])),
            "', '".join(sorted([x for x in list if len(x)==9])),
           )
        #print query
        c.execute(query)
        r = c.fetchone()
        return 0 if r is None or r[0] is None else r[0]
        
    def getAvgSize(self):
        c = self.cache.cursor()
        c.execute('SELECT SUM(size)/COUNT(*) FROM main.files AS fn WHERE NOT fn.isDir')
        r = c.fetchone()
        return 0 if r is None else r[0]
        
    def getMedianSize(self):
        c = self.cache.cursor()
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
        c = self.cache.cursor()
        c.execute('SELECT COUNT(*) AS cnt FROM main.files AS fn WHERE NOT fn.isDir GROUP BY fn.hash HAVING cnt>1')
        return sum(((cnt-1) for (cnt, ) in c.fetchall() if True))
        
    def getDuplicatedFilesSize(self):
        c = self.cache.cursor()
        c.execute('SELECT COUNT(*) AS cnt, size FROM main.files AS fn WHERE NOT fn.isDir GROUP BY fn.hash HAVING cnt>1')
        return sum(((size*(cnt-1)) for (cnt, size) in c.fetchall() if True))
        
    def getEmptyFilesCount(self):
        c = self.cache.cursor()
        c.execute('SELECT COUNT(*) AS cnt FROM main.files AS fn WHERE NOT fn.isDir AND size=0 GROUP BY fn.hash')
        r = c.fetchone()
        return 0 if r is None else r[0]
    
    def getTop10LargestFiles(self):
        c = self.cache.cursor()
        c.execute('SELECT fn.size, fn.path FROM main.files AS fn WHERE NOT fn.isDir ORDER BY fn.size DESC LIMIT 10')
        return c.fetchall()
    
    