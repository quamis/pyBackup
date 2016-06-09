# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os

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
        c.execute('CREATE TABLE files (path text, hash text)')


    def insertFileIntoFiles(self, path, h):
        c = self.conn.cursor()
        vals = (path, h)
        print vals
        c.execute('REPLACE INTO files VALUES (?, ?)', vals)
        #self.conn.commit()
    
    def findFileByPath(self, path):
        c = self.conn.cursor()
        vals = (path, )
        c.execute('SELECT path, hash FROM files WHERE path=?', vals)
        return c.fetchone()

    def getAll(self):
        c = self.conn.cursor()
        c.execute('SELECT path FROM files WHERE 1 ORDER BY path ASC')
        return c.fetchall()