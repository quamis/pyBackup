# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os

import Hasher.Hasher as Hasher
from Hasher.FastHashV1 import FastHashV1

class FastHashV1Cached(FastHashV1.FastHashV1):
    def __init__(self):
        self.dbExists = False;
        self.db = 'FastHashV1Cached.sqlite'
    
    def initialize(self):
	if os.path.isfile(self.db):
	    self.dbExists = True

	self.conn = sqlite3.connect(self.db)
	
	self.createTableFiles()
	
    def destroy(self):
        self.conn.commit()
	
    def createTableFiles(self):
	if not self.dbExists:
	    c = self.conn.cursor()
	    c.execute('CREATE TABLE files (path text, hash text)')


    def insertFileIntoFiles(self, path, h):
	c = self.conn.cursor()
	vals = (path.path, h)
	c.execute('INSERT INTO files VALUES (?, ?)', vals)
	#self.conn.commit()
	
    def fileFileByPath(self, path):
	c = self.conn.cursor()
	vals = (path.path, )
	c.execute('SELECT path, hash FROM files WHERE path=?', vals)
	return c.fetchone()

    def hash(self, path):
	h = self.fileFileByPath(path)
	if h:
	    print h[0]
	    return "Q"+h[0]
	else:
	    h = super(FastHashV1Cached, self).hash(path)
	    self.insertFileIntoFiles(path, h)
	    return h