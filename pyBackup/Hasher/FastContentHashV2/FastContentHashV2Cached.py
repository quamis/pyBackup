# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os
import hashlib
import time
from bases import Bases

from Hasher.FastContentHashV1 import FastContentHashV1Cached

class FastContentHashV2Cached(FastContentHashV1Cached.FastContentHashV1Cached):
    #def __init__(self):
    #    super(FastContentHashV1Cached, self).__init__()
        
    def _getHasherMapByExtension(self):
        return [
            {
                'ext':  ('.txt', '.csv', '.odt', '.img', '.sqlite', '.db'),
                'slots': [
                    { 'max':    0, 'read': 4.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, },   #   any size
                ],
            },
            
            {   # music
                'ext':  ('.mp3', '.mp4', '.avi', '.mpg', '.mpeg', '.ogg', '.wav'),
                'slots': [
                    #{ 'max':  Mb, 'read': Mb  , 'skip': Mb  , 'head': Mb  , 'tail': Mb  , },   # reads = (head+tail) + max*floor((max-(head+tail))/(read+skip))
                    { 'max':    2, 'read': 1.00, 'skip': 0.50, 'head': 0.50, 'tail': 0.25, },   # ~ TODO
                    { 'max':    4, 'read': 1.00, 'skip': 1.00, 'head': 1.00, 'tail': 0.50, },   # ~ TODO
                    { 'max':   16, 'read': 1.00, 'skip': 3.00, 'head': 1.00, 'tail': 0.50, },   # ~ TODO
                    { 'max':   64, 'read': 1.00, 'skip': 7.00, 'head': 1.00, 'tail': 0.50, },   # ~ TODO
                    { 'max':  128, 'read': 1.00, 'skip':15.00, 'head': 1.50, 'tail': 1.00, },   # ~ TODO
                    { 'max':  256, 'read': 1.00, 'skip':31.00, 'head': 2.00, 'tail': 1.50, },   # ~ TODO
                ],
            },
            
            {   # defaults
                'ext':  ('*', ),
                'slots': [
                    #{ 'max':  Mb, 'read': Mb  , 'skip': Mb  , 'head': Mb  , 'tail': Mb  , },   # reads = (head+tail) + max*floor((max-(head+tail))/(read+skip))
                    { 'max':    4, 'read': 1.00, 'skip': 1.00, 'head': 1.00, 'tail': 0.50, },   # ~ TODO
                    { 'max':   16, 'read': 1.00, 'skip': 3.00, 'head': 2.00, 'tail': 1.00, },   # ~ TODO
                    { 'max':  128, 'read': 2.00, 'skip': 6.00, 'head': 2.00, 'tail': 2.00, },   # ~ TODO
                    { 'max':  512, 'read': 2.00, 'skip':14.00, 'head': 4.00, 'tail': 4.00, },   # ~ TODO
                    { 'max': 4096, 'read': 2.00, 'skip':30.00, 'head': 8.00, 'tail': 8.00, },   # ~ TODO
                ],
            },
        ]
                
            
            
    def _getHashObj(self):
        return hashlib.sha1()
        
    def _getFinalHash(self, hashObj, path, readCfg, stats):
        bases = Bases()
        r = "FastContentHashV2,sha1:%s,ct:%s,mt:%s,sz:%s" % (hashObj.hexdigest(), bases.toBase62(path.ctime), bases.toBase62(path.mtime), bases.toBase62(path.size))
        return r
        