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


"""
    useful for VERY slow read-only FS's (like Google Photos)
"""
class FastAttributeHashV1(object):
    def initialize(self):
        pass
    
    def destroy(self):
        pass
    
    def _getHashObj(self):
        return hashlib.sha1()
        
    def _getFinalHash(self, hashObj, path):
        bases = Bases()
        return "FastAttributeHashV1,ct:%s,sz:%s" % (bases.toBase62(path.ctime), bases.toBase62(path.size), )
    
    def hash(self, path):
       return self._hash(path)
        
    def _hash(self, path):
         # match the file into one slot of the hasherMapByExtenstion
        hashObj = self._getHashObj()
        return self._getFinalHash(hashObj, path)
        