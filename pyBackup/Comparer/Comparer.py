# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import sqlite3
import os, time

class Comparer(object):
    def __init__(self):
        self.cacheOld = None
        self.cacheNew = None
        self.conn = None
        
    def setOldCache(self, cache):
        self.cacheOld = cache

    def setNewCache(self, cache):
        self.cacheNew = cache

    def initialize(self):
        self.conn = sqlite3.connect(self.cacheNew.db)
        c = self.conn.cursor()
        c.execute('ATTACH DATABASE ? AS old', (self.cacheOld.db, ))
    
    def destroy(self):
        self.conn.commit()
        self.conn.close()
        
    def getAllMoved(self):
        c = self.conn.cursor()
        c.execute('SELECT fn.path, fo.path FROM main.files AS fn LEFT JOIN old.files AS fo ON fn.hash = fo.hash WHERE NOT fo.isDir AND NOT fn.isDir AND fo.path!=fn.path')
        return c.fetchall()
    
    def movePath(self, opath, npath):
        c = self.conn.cursor()
        vals=(npath, opath)
        c.execute('UPDATE old.files SET path=? WHERE NOT isDir AND path=?', vals)
    
    def getAllChanged(self):
        c = self.conn.cursor()
        c.execute('SELECT fn.path, fo.path FROM main.files AS fn INNER JOIN old.files AS fo ON fn.path = fo.path WHERE NOT fo.isDir AND NOT fn.isDir AND fo.hash!=fn.hash')
        return c.fetchall()
    
    def getAllNew(self):
        c = self.conn.cursor()
        c.execute('SELECT path FROM main.files WHERE NOT isDir AND path NOT IN (SELECT path FROM old.files WHERE NOT isDir)')
        return c.fetchall()
    
    def getAllDeleted(self):
        c = self.conn.cursor()
        c.execute('SELECT path FROM old.files WHERE NOT isDir AND path NOT IN (SELECT path FROM main.files WHERE NOT isDir)')
        return c.fetchall()
    