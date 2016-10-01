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

class FastContentHashV1(object):
    def initialize(self):
        pass
    
    def destroy(self):
        pass
    
    def _getHasherMapByExtension(self):
        return [
            {
                'ext':  ('.txt', '.csv', '.odt', '.img', '.sqlite', '.db'),
                'slots': [
                    { 'max':    0, 'read': 4.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, },   #   any size
                ],
            },
            
            {   # defaults
                'ext':  ('*', ),
                'slots': [
                    #{ 'max':  Mb, 'read': Mb  , 'skip': Mb  , 'head': Mb  , 'tail': Mb  , },   # reads = (head+tail) + max*floor((max-(head+tail))/(read+skip))
                    { 'max':    4, 'read': 4.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, },   #   ~4
                    { 'max':    8, 'read': 4.00, 'skip': 0.10, 'head': 1.00, 'tail': 1.00, },   #   ~6
                    { 'max':   16, 'read': 4.00, 'skip': 0.25, 'head': 1.00, 'tail': 1.00, },   #  ~14
                    { 'max':   32, 'read': 4.00, 'skip': 0.50, 'head': 2.00, 'tail': 2.00, },   #  ~28
                    { 'max':  128, 'read': 4.00, 'skip': 1.00, 'head': 2.00, 'tail': 2.00, },   # ~100
                    { 'max':  256, 'read': 4.00, 'skip': 2.00, 'head': 2.00, 'tail': 2.00, },   # ~172
                    { 'max':  512, 'read': 4.00, 'skip': 4.00, 'head': 2.00, 'tail': 5.00, },   # ~259
                    { 'max': 1024, 'read': 4.00, 'skip': 8.00, 'head':16.00, 'tail': 5.00, },   # ~353
                    { 'max': 4096, 'read': 4.00, 'skip':32.00, 'head': 8.00, 'tail': 8.00, },   # ~468
                ],
            },
        ]
                
            
            
    def _getHashObj(self):
        return hashlib.sha1()
        
    def _getFinalHash(self, hashObj, path, readCfg, stats):
        bases = Bases()
        return "FastContentHashV1,sha1:%s,sz:%s" % (hashObj.hexdigest(), bases.toBase62(path.size))
    
    def _getHasherMapCfg(self, path):
        readCfg = { 'max': 0, 'read': 0.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, 'slot:cfg': {}}
        hasherMapByExtenstion = self._getHasherMapByExtension()
        for slot in hasherMapByExtenstion:
            if (os.path.splitext(path.path)[1].lower() in slot['ext']) or (slot['ext']==('*', )):
                #print slot['ext']
                #print slot['slots']
                readCfg = slot['slots'][0]
                for cfg in slot['slots']:
                    readCfg = cfg
                    
                    readCfg['slot:cfg'] = {}
                    if 'cfg' in slot:
                        readCfg['slot:cfg'] = slot['cfg']
                        
                    if path.size/(1*1024*1024)<cfg['max']:
                        break
                break
        return readCfg
    
    def hash(self, path):
       return self._hash(path)
        
    def _hash(self, path):
         # match the file into one slot of the hasherMapByExtenstion
        readCfg = self._getHasherMapCfg(path)
        hashObj = self._getHashObj()
        stats = self._hashFileContent(path, hashObj, readCfg)
        return self._getFinalHash(hashObj, path, readCfg, stats)
        
        
    def _hashFileContent(self, path, hashObj, readCfg):
        stats = {
            'head_cnt':0,
            'head_sz': 0,
            'tail_cnt':0,
            'tail_sz': 0,
            'data_cnt':0,
            'data_sz': 0,
        }

        fi = open(path.path, 'rb')
        
        size = path.size
        limit = size
        if 'limit:head' in readCfg['slot:cfg']:
            limit = min(readCfg['slot:cfg']['limit:head']*1024*1024, path.size)
        
        #print "rsize,limit %.2fMb, %.2fMb" % (path.size/float(1024*1024), limit/float(1024*1024))
        
        cpos = 0
        while True:
            if readCfg['head'] and cpos<=readCfg['head']*1024*1024:
                data = fi.read(int(readCfg['head']*1024*1024))
                dl = len(data)
                cpos+= dl
                stats['head_cnt']+= 1
                stats['head_sz']+=  dl
            elif readCfg['tail'] and cpos>=(size - (readCfg['skip']*1024*1024) - (readCfg['tail']*1024*1024)):
                data = fi.read(int(readCfg['tail']*1024*1024))
                dl = len(data)
                cpos+= dl
                stats['tail_cnt']+= 1
                stats['tail_sz']+=  dl
            else:
                data = fi.read(int(readCfg['read']*1024*1024))
                dl = len(data)
                cpos+= dl
                stats['data_cnt']+= 1
                stats['data_sz']+=  dl
                
            if not data:
                break
            
            hashObj.update(data)
            
            if cpos>limit:
                break
            
            if readCfg['skip']:
                fi.seek(readCfg['skip']*1024*1024, os.SEEK_CUR)
                cpos+=readCfg['skip']*1024*1024
        
        fi.close()

        return stats
    
