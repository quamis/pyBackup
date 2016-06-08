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
        md5 = hashlib.md5()
        while True:
            data = fi.read(1*1024*1024)
            if not data:
                break
            md5.update(data)
            
        return "FastHashV1,ct:%d,mt:%d,sz:%s,md5:%s"%(path.ctime, path.mtime, path.size, md5.hexdigest())
    
