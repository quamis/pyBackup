# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os, time

class SimpleComparer(object):
    def __init__(self):
        self.cacheOld = None
        self.cacheNew = None
        
    def setOldCache(self, cache):
        self.cacheOld = cache

    def setNewCache(self, cache):
        self.cacheNew = cache

    def initialize(self):
        c = self.cacheNew.cursor()
        c.execute('ATTACH DATABASE ? AS old', (self.cacheOld.db, ))
    
    def destroy(self):
        self.cacheNew.commit()
        
    def commit(self):
        self.cacheNew.commit()
        
        
    def getMovedFiles(self):
        c = self.cacheNew.cursor()
        c.execute('''
            SELECT 
                fn.path, fo.path, fn.size, fo.size
            FROM main.files AS fn 
                LEFT JOIN old.files AS fo ON fn.hash=fo.hash 
            WHERE 
                NOT fo.isDir 
                AND NOT fn.isDir 
                AND fo.path!=fn.path 
                AND fn.path NOT IN (SELECT path FROM old.files)
                AND fo.path NOT IN (SELECT path FROM main.files)
            GROUP BY fo.path
            ''')
        return c.fetchall()
    
    def moveFile(self, opath, npath):
        c = self.cacheNew.cursor()
        vals=(npath.path, opath.path)
        # TODO: load all attributes, not just paths (mtime, ctime, etc)
        c.execute('UPDATE old.files SET path=? WHERE NOT isDir AND path=?', vals)
    
    def getChangedFiles(self):
        c = self.cacheNew.cursor()
        c.execute('SELECT fn.path, fo.path, fn.size, fo.size FROM main.files AS fn INNER JOIN old.files AS fo ON fn.path = fo.path WHERE NOT fo.isDir AND NOT fn.isDir AND fo.hash!=fn.hash')
        return c.fetchall()
    
    def updateFile(self, opath, npath):
        c = self.cacheNew.cursor()
        vals=(npath.path, opath.path)
        c.execute('UPDATE old.files SET hash=(SELECT hash FROM main.files WHERE path=? LIMIT 1) WHERE NOT isDir AND path=?', vals)
    
    def getNewFiles(self):
        c = self.cacheNew.cursor()
        c.execute('SELECT path, size FROM main.files WHERE NOT isDir AND path NOT IN (SELECT path FROM old.files WHERE NOT isDir)')
        return c.fetchall()
    
    def getNewDirs(self):
        c = self.cacheNew.cursor()
        c.execute('SELECT path FROM main.files WHERE isDir AND path NOT IN (SELECT path FROM old.files WHERE isDir) ORDER BY LENGTH(path) ASC, path ASC')
        return c.fetchall()
    
    def _newPath(self, npath):
        c = self.cacheNew.cursor()
        vals=(npath, )
        c.execute('REPLACE INTO old.files (hash, path, isDir, ctime, mtime, atime, size) SELECT hash, path, isDir, ctime, mtime, atime, size FROM main.files WHERE path=? LIMIT 1', vals)
        
    def newFile(self, npath):
        return self._newPath(npath.path)
    
    def newDir(self, npath):
        return self._newPath(npath.path)
    
    
    def getDeletedFiles(self):
        c = self.cacheNew.cursor()
        c.execute('SELECT path, size FROM old.files WHERE NOT isDir AND path NOT IN (SELECT path FROM main.files WHERE NOT isDir)')
        return c.fetchall()
    
    def getDeletedDirs(self):
        c = self.cacheNew.cursor()
        c.execute('SELECT path FROM old.files WHERE isDir AND path NOT IN (SELECT path FROM main.files WHERE isDir) ORDER BY LENGTH(path) DESC, path ASC')
        return c.fetchall()
    
    def deleteFile(self, opath):
        c = self.cacheNew.cursor()
        vals=(opath.path, )
        c.execute('DELETE FROM old.files WHERE NOT isDir AND path=?', vals)
        
    def deleteDir(self, opath):
        c = self.cacheNew.cursor()
        vals=(opath.path, )
        c.execute('DELETE FROM old.files WHERE isDir AND path=?', vals)
        
        
        