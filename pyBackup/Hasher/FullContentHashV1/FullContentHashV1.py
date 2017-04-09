# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os
import hashlib
import time
from bases import Bases


import Hasher.Hasher as Hasher

class FullContentHashV1(object):
    def initialize(self):
        pass
    
    def destroy(self):
        pass
        
    def hash(self, path):
        try:
            fi = open(path.path, 'rb')
        except IOError:
            return "FileNotFound"
            
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha512 = hashlib.sha512()

        cpos = 0
        while True:
            data = fi.read(int(1*1024*1024))
            dl = len(data)
            cpos+= dl
            if not data:
                break
            
            md5.update(data)
            sha1.update(data)
            sha512.update(data)

        fi.close()
        
        bases = Bases()
        return "FullContentHashV1,md5:%s,sha1:%s,sha512:%s,sz:%s" % (md5.hexdigest(), sha1.hexdigest(), sha512.hexdigest(), bases.toBase16(path.size))
        
