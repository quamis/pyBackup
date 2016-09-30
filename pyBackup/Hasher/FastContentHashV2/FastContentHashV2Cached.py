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
        
    def _hash(self, path):
         # match the file into one slot of the hasherMapByExtenstion
        readCfg = self._getHasherMapCfg(path)
        
        strategy = 'default'
        if 'strategy' in readCfg:
            strategy = readCfg['strategy']
        
        ret = None
        if strategy=='default':
            hashObj = self._getHashObj()
            stats = self._hashFileContent(path, hashObj, readCfg)
            ret = self._getFinalHash_default(hashObj, path, readCfg, stats)
        elif strategy=='ignore:mtime':
            hashObj = self._getHashObj()
            stats = self._hashFileContent(path, hashObj, readCfg)
            ret = self._getFinalHash_ignore_mtime(hashObj, path, readCfg, stats)
        elif strategy=='ignore:hash':
            ret = self._getFinalHash_ignore_hash(None, path, readCfg, None)
        else:
            raise Exception('Invalid hashing strategy requested') 
        
        #print ret
        return ret
        
    def _getHashObj(self):
        return hashlib.sha1()
        
    def _getFinalHash_default(self, hashObj, path, readCfg, stats):
        bases = Bases()
        return "FCHV2,sha1:%s,mt:%s,sz:%s" % (hashObj.hexdigest(), bases.toBase62(path.mtime*1000), bases.toBase62(path.size))
        
    def _getFinalHash_ignore_mtime(self, hashObj, path, readCfg, stats):
        bases = Bases()
        return "FCHV2,sha1:%s,sz:%s" % (hashObj.hexdigest(), bases.toBase62(path.size))
        
    def _getFinalHash_ignore_hash(self, hashObj, path, readCfg, stats):
        bases = Bases()
        return "FCHV2,mt:%s,ct:%s,sz:%s" % (bases.toBase62(path.mtime*1000), bases.toBase62(path.ctime*1000), bases.toBase62(path.size))
        
    def _getHasherMapByExtension(self):
        return [
            {
                'ext':  (
                    '.txt', '.csv', '.odt', '.ods', '.doc', '.xls', '.rtf',
                    '.sqlite', '.db', 
                    '.py', '.php', '.js', '.html', '.htm', '.css', '.xml', 
                 ),
                'slots': [
                    { 'max':    0, 'read': 4.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, 'strategy':'ignore:mtime', },   #   any size
                ],
            },
            
            {   # music
                'ext':  (
                    '.mp3', '.mp4', '.m4a', '.ogg', '.wav', '.flac', '.ape', 
                    '.avi', '.mpg', '.mpeg', '.3gp', '.flv', '.wma',
                    '.iso', '.cue', '.bin', '.img', 
                    '.rar', '.zip', '.tgz', '.gz', '.gzip', '.7z', '.tbz', 'xz', 
                    '.xcf', '.png', '.jpg', '.jpeg', '.gif', '.bmp',
                    '.pdf', '.ps', 
                    '.epub', '.mobi', '.cbz', '.cbr', 
                ),
                'slots': [
                    #{ 'max':  Mb, 'read': Mb  , 'skip': Mb  , 'head': Mb  , 'tail': Mb  , },   # reads = (head+tail) + max*floor((max-(head+tail))/(read+skip))
                    #{ 'max':    1, 'read': 0.00, 'skip': 64.00, 'head': 0.00, 'tail': 0.00, },   #   any size
                    
                    { 'max':    1, 'read': 0.25, 'skip':  0.25, 'head': 0.10, 'tail': 0.10, 'strategy':'ignore:hash', },   # ~ TODO
                    { 'max':    2, 'read': 0.50, 'skip':  0.50, 'head': 0.20, 'tail': 0.25, 'strategy':'ignore:hash', },   # ~ TODO
                    { 'max':    4, 'read': 0.50, 'skip':  1.50, 'head': 0.25, 'tail': 0.20, 'strategy':'ignore:hash', },   # ~ TODO
                    { 'max':   16, 'read': 1.00, 'skip':  3.00, 'head': 0.50, 'tail': 0.25, 'strategy':'ignore:hash', },   # ~ TODO
                    { 'max':   64, 'read': 1.00, 'skip': 15.00, 'head': 0.50, 'tail': 0.50, 'strategy':'ignore:hash', },   # ~ TODO
                    { 'max':  128, 'read': 1.00, 'skip': 31.00, 'head': 1.50, 'tail': 1.00, 'strategy':'ignore:hash', },   # ~ TODO
                    { 'max':  256, 'read': 1.00, 'skip': 63.00, 'head': 2.00, 'tail': 1.50, 'strategy':'ignore:hash', },   # ~ TODO
                    { 'max': 1024, 'read': 1.00, 'skip':127.00, 'head': 4.00, 'tail': 4.00, 'strategy':'ignore:hash', },   # ~ TODO

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