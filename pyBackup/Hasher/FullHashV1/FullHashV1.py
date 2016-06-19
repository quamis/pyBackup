# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os
import hashlib
from bases import Bases

import Hasher.Hasher as Hasher

class FullHashV1(object):
    def initialize(self):
        pass
    
    def destroy(self):
        pass
        
    def hash(self, path):
        fi = open(path.path, 'rb')
        md5 = hashlib.md5()
        bases = Bases()
        while True:
            data = fi.read(4*1024*1024)
            if not data:
                break
            md5.update(data)
            
        return "FastContentHashV1,sz:%06s,md5:%s" % (bases.toBase62(path.size), md5.hexdigest())
   
