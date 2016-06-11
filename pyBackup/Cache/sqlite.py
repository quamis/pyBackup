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
        self.initialized = False
    
    def initialize(self):
        if not self.initialized:
            print "sqlite.initialize"
            if os.path.isfile(self.db):
                self.dbExists = True

            self.conn = sqlite3.connect(self.db)
            if not self.dbExists:
                self.createTableFiles()
            
            self.initialized = True
    
    def destroy(self):
        self.conn.commit()
        
    def setCacheLocation(self, db):
        self.db = db
    
    def createTableFiles(self):
        c = self.conn.cursor()
        c.execute('CREATE TABLE files (hash TEXT, path TEXT, isDir INTEGER, ctime FLOAT, mtime FLOAT, size INTEGER, time FLOAT)')


    def insertFileIntoFiles(self, p, h):
        c = self.conn.cursor()
        vals = (h, p.path, p.isDir, p.ctime, p.mtime, p.size, time.time())
        c.execute('REPLACE INTO files VALUES (?, ?, ?, ?, ?, ?, ?)', vals)
        #self.conn.commit()
        
    def updateFileHashIntoFiles(self, p, h):
        c = self.conn.cursor()
        vals = (h, p.path)
        c.execute('UPDATE files SET hash=? WHERE path=?', vals)
        #self.conn.commit()
    
    def findFileByPath(self, path):
        c = self.conn.cursor()
        vals = (path, )
        c.execute('SELECT hash, path, isDir, ctime, mtime, size, time FROM files WHERE path=?', vals)
        return c.fetchone()

    def getAll(self):
        c = self.conn.cursor()
        c.execute('SELECT hash, path, isDir, ctime, mtime, size, time FROM files WHERE 1 ORDER BY time ASC')
        return c.fetchall()
    