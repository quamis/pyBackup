# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import hashlib
import time
from bases import Bases

from Hasher.FastContentHashV2 import FastContentHashV2Cached

class FastContentHashV3Cached(FastContentHashV2Cached.FastContentHashV2Cached):
    def _getFinalHash_ignore_hash(self, hashObj, path, readCfg, stats):
        bases = Bases()
        return "FCHV2,mt:%s,ct:%s,sz:%s" % (bases.toBase62(path.mtime*1000), bases.toBase62(path.ctime*1000), bases.toBase62(path.size))
          