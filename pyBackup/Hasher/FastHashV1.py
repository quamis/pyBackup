# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os
import hashlib

import Hasher

class Base(object):
    def initialize(self):
        pass
    
    def destroy(self):
        pass
        
    def hash(self, path):
	fi = open(path.path, 'rb')
        sha1 = hashlib.sha1()
        while True:
            data = fi.read(1*1024*1024)
            if not data:
                break
            sha1.update(data)
            
        return "FastHashV1,ct:%d,mt:%d,sz:%s,sha1:%s"%(path.ctime, path.mtime, path.size, sha1.hexdigest())
    

class Cached(Base):
    def __init__(self):
        self.db = None
        super(Cached, self).__init__()
    
    def initialize(self):
        super(Cached, self).initialize()
    
    def destroy(self):
        super(Cached, self).destroy()
        
    def setCache(self, cache):
        self.db = cache
    
    def hash(self, path):
        h = self.db.findFileByPath(path.path)
        if h[0]:
            return h[0]
        else:
            h = super(Cached, self).hash(path)
            self.db.updateFileHashIntoFiles(path, h)
            return h
