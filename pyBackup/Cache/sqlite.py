# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os, time
import logging

class sqlite(object):
    def __init__(self):
        self.dbExists = False;
        self.db = None
        self.conn = None
        self.initialized = False
        self.curr = None
    
    def initialize(self):
        if not self.initialized:
            logging.debug("sqlite.initialize")
            if os.path.isfile(self.db):
                logging.debug("sqlite: db exists")
                self.dbExists = True

            self.conn = sqlite3.connect(self.db, isolation_level="EXCLUSIVE")
            if not self.dbExists:
                logging.debug("sqlite: db dooesn't exist")
                logging.debug("sqlite: createTableFiles")
                self.createTableFiles()
            
            self.initialized = True
    
    def destroy(self):
        self.commit()
        self.conn.close()
        
    def commit(self):
        self.conn.commit()
        self.curr = None
        
    def _pathCleanup(self, p):
        return p
    
    def cursor(self):
        #return self.conn.cursor()
        if self.curr is None:
            self.curr = self.conn.cursor()
        return self.curr
        
        
    def setCacheLocation(self, db):
        self.db = db
    
    def createTableFiles(self):
        c = self.cursor()
        c.execute('''CREATE TABLE files (
            hash TEXT, 
            path TEXT, 
            isDir INTEGER, 
            ctime FLOAT, 
            mtime FLOAT, 
            atime FLOAT, 
            size INTEGER, 
            PRIMARY KEY (path)
        )''')
        self.commit()
        
        c.execute('''CREATE TABLE fullHashes (
            path TEXT, 
            fullHash TEXT,
            PRIMARY KEY (path)
        )''')
        self.commit()
        
        c.execute('''CREATE TABLE tags (
            path TEXT, 
            key TEXT,
            value TEXT,
            PRIMARY KEY (path)
        )''')
        self.commit()

        c.execute('''CREATE TABLE log (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            message STRING  NOT NULL,
            time    FLOAT
        )''')
        self.commit()
        
        c.execute('''CREATE TABLE flags (
            id    STRING PRIMARY KEY,
            value STRING
        )''')
        self.commit()

        
    def setFlag(self, k, v):
        c = self.cursor()
        vals = (k, v)
        c.execute('REPLACE INTO flags VALUES (?, ?)', vals)
        
    def getFlag(self, k):
        c = self.cursor()
        vals = (k, )
        c.execute('SELECT value FROM flags WHERE id=?', vals)
        r = c.fetchone()
        return None if r is None else r[0]
        
    def log(self, msg):
        c = self.cursor()
        vals = (msg, time.time())
        c.execute('INSERT INTO log (message, time) VALUES (?, ?)', vals)
        
    def insertFileIntoFiles(self, p, h):
        c = self.cursor()
        vals = (h, self._pathCleanup(p.path), p.isDir, p.ctime, p.mtime, p.atime, p.size)
        c.execute('REPLACE INTO files VALUES (?, ?, ?, ?, ?, ?, ?)', vals)
        
        vals = (self._pathCleanup(p.path), "%.3f" % (time.time()))
        c.execute('INSERT OR IGNORE INTO tags VALUES (?, "time", ?)', vals)
        
    def deleteFileFromFiles(self, p):
        c = self.cursor()
        vals = (self._pathCleanup(p.path), )
        c.execute('DELETE FROM files WHERE path=?', vals)
        
        vals = (self._pathCleanup(p.path), )
        c.execute('DELETE FROM tags WHERE path=?', vals)
        
        vals = (self._pathCleanup(p.path), )
        c.execute('DELETE FROM fullHashes WHERE path=?', vals)
        
        
    def updateFileHashIntoFiles(self, p, h):
        c = self.cursor()
        vals = (h, self._pathCleanup(p.path))
        c.execute('UPDATE files SET hash=? WHERE path=?', vals)
        
    def updateFileFullHashIntoFiles(self, p, h):
        c = self.cursor()
        vals = (self._pathCleanup(p.path), h, )
        c.execute('REPLACE INTO fullHashes VALUES (?, ?)', vals)
    
    def findFileByPath(self, path):
        c = self.cursor()
        vals = (self._pathCleanup(path), )
        print vals
        c.execute('SELECT hash, path, isDir, ctime, mtime, atime, size FROM files WHERE path=?', vals)
        return c.fetchone()
        
    def getAll(self):
        c = self.cursor()
        c.execute('SELECT hash, path, isDir, ctime, mtime, atime, size FROM files WHERE 1 ORDER BY path ASC')
        return c.fetchall()
        
    def resetFilesData(self):
        c = self.cursor()
        c.execute('DELETE FROM files')
        # c.execute('DELETE FROM tags')
        
    def optimize(self):
        c = self.cursor()
        c.execute('VACUUM')
        
    def removeOldLeafs(self):
        c = self.cursor()
        c.execute('DELETE FROM fullHashes WHERE path NOT IN (SELECT f.path FROM files AS f)')
        self.commit()
        c.execute('DELETE FROM tags WHERE path NOT IN (SELECT f.path FROM files AS f)')
        self.commit()
        