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
                'ext':  (
                    '.txt', '.csv', '.odt', '.sqlite', '.db', '.py', '.php', '.js', '.html', '.htm', '.css', '.xml',
                 ),
                'slots': [
                    { 'max':    0, 'read': 4.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, },   #   any size
                ],
            },
            
            {   # music
                'ext':  (
                    '.mp3', '.mp4', '.m4a', '.avi', '.mpg', '.mpeg', '.ogg', '.wav', '.flac', '.ape', '.3gp',
                    '.iso', '.cue', '.bin', '.img', 
                    '.rar', '.zip', '.tgz', '.gz', '.gzip', '.7z', '.tbz', 'xz', 
                    '.xcf', '.png', '.jpg', '.jpeg', '.gif', '.bmp',
                    '.pdf', 
                    '.epub', '.mobi', 
                ),
                'slots': [
                    #{ 'max':  Mb, 'read': Mb  , 'skip': Mb  , 'head': Mb  , 'tail': Mb  , },   # reads = (head+tail) + max*floor((max-(head+tail))/(read+skip))
                    #{ 'max':    1, 'read': 0.00, 'skip': 64.00, 'head': 0.00, 'tail': 0.00, },   #   any size
                    
                    { 'max':    1, 'read': 0.25, 'skip':  0.25, 'head': 0.10, 'tail': 0.10, },   # ~ TODO
                    { 'max':    2, 'read': 0.50, 'skip':  0.50, 'head': 0.20, 'tail': 0.25, },   # ~ TODO
                    { 'max':    4, 'read': 0.50, 'skip':  1.50, 'head': 0.25, 'tail': 0.20, },   # ~ TODO
                    { 'max':   16, 'read': 1.00, 'skip':  3.00, 'head': 0.50, 'tail': 0.25, },   # ~ TODO
                    { 'max':   64, 'read': 1.00, 'skip': 15.00, 'head': 0.50, 'tail': 0.50, },   # ~ TODO
                    { 'max':  128, 'read': 1.00, 'skip': 31.00, 'head': 1.50, 'tail': 1.00, },   # ~ TODO
                    { 'max':  256, 'read': 1.00, 'skip': 63.00, 'head': 2.00, 'tail': 1.50, },   # ~ TODO
                    { 'max': 1024, 'read': 1.00, 'skip':127.00, 'head': 4.00, 'tail': 4.00, },   # ~ TODO

                ],
            },
            
            {   # defaults
                'ext':  ('*', ),
                'slots': [
                    #{ 'max':  Mb, 'read': Mb  , 'skip': Mb  , 'head': Mb  , 'tail': Mb  , },   # reads = (head+tail) + max*floor((max-(head+tail))/(read+skip))
                    { 'max':    1, 'read': 0.25, 'skip':  0.25, 'head': 0.25, 'tail': 0.25, },   # ~ TODO
                    { 'max':    2, 'read': 0.50, 'skip':  0.50, 'head': 0.25, 'tail': 0.25, },   # ~ TODO
                    { 'max':   16, 'read': 1.00, 'skip':  1.00, 'head': 1.50, 'tail': 1.50, },   # ~ TODO
                    { 'max':  128, 'read': 1.00, 'skip':  4.00, 'head': 4.00, 'tail': 4.00, },   # ~ TODO
                    { 'max': 1024, 'read': 1.00, 'skip': 64.00, 'head': 4.00, 'tail': 4.00, },   # ~ TODO
                ],
            },
        ]
                
            
            
    def _getHashObj(self):
        return hashlib.sha1()
        
    def _getFinalHash(self, hashObj, path, readCfg, stats):
        bases = Bases()
        r = "FastContentHashV2,sha1:%s,mt:%s,sz:%s" % (hashObj.hexdigest(), bases.toBase62(path.mtime*1000), bases.toBase62(path.size))
        return r
        