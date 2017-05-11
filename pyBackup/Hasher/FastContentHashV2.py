# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os
import hashlib
import time
from bases import Bases

import Hasher
import FastContentHashV1

class Cached(FastContentHashV1.Cached):
    def _hash(self, path):
         # match the file into one slot of the hasherMapByExtenstion
        readCfg = self._getHasherMapCfg(path)
        
        strategy = 'default'
        if 'strategy' in readCfg['slot:cfg']:
            strategy = readCfg['slot:cfg']['strategy']
        
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
        
        h = hashObj.hexdigest()
        if 'limit:head' in readCfg['slot:cfg']:
            h = h[0:16]
            #print "i have read %.2fMb" % ((stats['head_sz']+stats['data_sz']+stats['tail_sz'])/float(1024*1024))
            return "FCHV2,sha1f:%s,mt:%s,sz:%s" % (h, bases.toBase62(path.mtime*1000), bases.toBase62(path.size))
        
        return "FCHV2,sha1:%s,mt:%s,sz:%s" % (h, bases.toBase62(path.mtime*1000), bases.toBase62(path.size))
        
    def _getFinalHash_ignore_mtime(self, hashObj, path, readCfg, stats):
        bases = Bases()
        return "FCHV2,sha1:%s,sz:%s" % (hashObj.hexdigest(), bases.toBase62(path.size))
        
    def _getFinalHash_ignore_hash(self, hashObj, path, readCfg, stats):
        bases = Bases()
        stat = os.stat(path.path)
        return "FCHV2,mt:%s,ct:%s,sz:%s,id:%s" % (bases.toBase62(path.mtime*1000), bases.toBase62(path.ctime*1000), bases.toBase62(path.size), bases.toBase62(stat.st_ino))
        
    def _getHasherMapByExtension(self):
        optimizedReadCfg = [
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

        ]
        
        return [
            {   'ext':  (       # do the complete hashing algo (no skips)
                    '.txt', '.csv', '.odt', '.ods', '.doc', '.xls', '.rtf',
                    '.sqlite', '.db', 
                    '.py', '.php', '.js', '.html', '.htm', '.css', '.xml', 
                 ),
                'slots': [
                    { 'max':    0, 'read': 4.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, 'strategy':'ignore:mtime', },   #   any size, rehash completly, but ignore mtime
                ],
            },
            
            {   'ext':  (       # do a limited hashing for the head only
                    '.iso', '.cue', '.bin', '.img', 
                    '.rar', '.zip', '.tgz', '.gz', '.gzip', '.7z', '.tbz', 'xz', 
                    '.xcf', '.psd', '.nef', '.raf',                             # photos
                ),
                'cfg': {
                    'strategy':'default', 
                    'limit:head':  0.25, 
                 },
                'slots': optimizedReadCfg,
            },
                
            {   'ext':  (       # skip hashing alltogether
                    '.mp3', '.mp4', '.m4a', '.m4v', '.ogg', '.wav', '.flac', '.ape', 
                    '.avi', '.mpg', '.mpeg', '.3gp', '.flv', '.wma', '.mov',
                    '.pdf', '.ps', 
                    '.epub', '.mobi', '.cbz', '.cbr', 
                    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif',    # photos
                ),
                'cfg': {
                    'strategy':'ignore:hash', 
                 },
                'slots': optimizedReadCfg,
            },
            
            {   # defaults
                'ext':  ('*', ),
                'slots': optimizedReadCfg,
            },
        ]
                
                
                
                
                
                
class Cached_noInode(Cached):
    def _getFinalHash_ignore_hash(self, hashObj, path, readCfg, stats):
        bases = Bases()
        return "FCHV2,mt:%s,ct:%s,sz:%s" % (bases.toBase62(path.mtime*1000), bases.toBase62(path.ctime*1000), bases.toBase62(path.size))
          
