# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os
import hashlib

import Hasher.Hasher as Hasher

class FastHashV1(object):
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
    
