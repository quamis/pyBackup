# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os, time

class sqlite(object):
    def __init__(self):
        self.dbExists = False;
        self.db = None
        self.conn = None
        self.initialized = False
        self.curr = None
    
    def initialize(self):
        if not self.initialized:
            print "sqlite.initialize()"
            if os.path.isfile(self.db):
                print "sqlite.dbExists"
                self.dbExists = True

            self.conn = sqlite3.connect(self.db, isolation_level="EXCLUSIVE")
            if not self.dbExists:
                print "sqlite.createTableFiles()"
                self.createTableFiles()
            
            self.initialized = True
    
    def destroy(self):
        self.commit()
        self.conn.close()
        
    def commit(self):
        self.conn.commit()
        self.curr = None
    
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


    def insertFileIntoFiles(self, p, h):
        c = self.cursor()
        vals = (h, p.path, p.isDir, p.ctime, p.mtime, p.size)
        c.execute('REPLACE INTO files VALUES (?, ?, ?, ?, ?, ?)', vals)
        
        vals = (p.path, "%.3f" % (time.time()))
        c.execute('INSERT OR IGNORE INTO tags VALUES (?, "time", ?)', vals)
        
    def updateFileHashIntoFiles(self, p, h):
        c = self.cursor()
        vals = (h, p.path)
        c.execute('UPDATE files SET hash=? WHERE path=?', vals)
        
    def updateFileFullHashIntoFiles(self, p, h):
        c = self.cursor()
        vals = (p.path, h, )
        c.execute('REPLACE INTO fullHashes VALUES (?, ?)', vals)
    
    def findFileByPath(self, path):
        c = self.cursor()
        vals = (path, )
        c.execute('SELECT hash, path, isDir, ctime, mtime, size FROM files WHERE path=?', vals)
        return c.fetchone()
        
    def getAll(self):
        c = self.cursor()
        c.execute('SELECT hash, path, isDir, ctime, mtime, size FROM files WHERE 1 ORDER BY time ASC')
        return c.fetchall()
        
    def resetFilesData(self):
        c = self.cursor()
        c.execute('DELETE FROM files')
        c.execute('DELETE FROM tags')