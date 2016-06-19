# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013
@author: lucian
'''
import os
import hashlib
from bases import Bases

import Hasher.Hasher as Hasher

class FastContentHashV1(object):
    def initialize(self):
        pass
    
    def destroy(self):
        pass
        
    def hash(self, path):
        hasherMapByExtenstion = [
            {
                'ext':  ('.txt','.csv', '.img', '.sqlite', '.db'),
                'slots': [
                    { 'max':    0, 'read': 2.00, 'skip': 0.00, 'head': 2.00, 'tail': 2.00, },   #   any size
                ],
            },
            
            {   # defaults
                'ext':  ('*', ),
                'slots': [
                    #{ 'max':  Mb, 'read': Mb  , 'skip': Mb  , 'head': Mb  , 'tail': Mb  , },   #   
                    { 'max':   10, 'read': 2.00, 'skip': 0.00, 'head': 2.00, 'tail': 2.00, },   #   10Mb, reads  10Mb
                    { 'max':   20, 'read': 2.00, 'skip': 0.10, 'head': 1.00, 'tail': 1.00, },   #   20Mb, reads  18Mb
                    { 'max':  100, 'read': 2.00, 'skip': 0.25, 'head': 2.00, 'tail': 2.00, },   #  100Mb, reads  82Mb
                    { 'max':  200, 'read': 2.00, 'skip': 0.50, 'head': 2.00, 'tail': 5.00, },   #  200Mb, reads 160Mb
                    { 'max':  500, 'read': 2.00, 'skip': 1.00, 'head': 2.00, 'tail': 5.00, },   #  500Mb, reads 333Mb
                    { 'max': 1000, 'read': 2.00, 'skip': 2.00, 'head':16.00, 'tail': 5.00, },   # 1000Mb, reads 500Mb
                    { 'max': 4000, 'read': 2.00, 'skip': 8.00, 'head':16.00, 'tail': 5.00, },   # 4000Mb, reads 800Mb
                ],
            },
        ]
        
        # match the file into one slot of the hasherMapByExtenstion
        readCfg = { 'max': 0, 'read': 0.00, 'skip': 0.00, 'head': 0.00, 'tail': 0.00, },   
        for slot in hasherMapByExtenstion:
            if (os.path.splitext(path.path)[1].lower() in slot['ext']) or (slot['ext']==('*', )):
                #print slot['ext']
                #print slot['slots']
                readCfg = slot['slots'][0]
                for cfg in slot['slots']:
                    readCfg = cfg
                    if path.size/(1*1024*1024)<cfg['max']:
                        break
                break
        
        fi = open(path.path, 'rb')
        hash = hashlib.sha1()

        cpos = 0
        while True:
            if cpos<=readCfg['head']*1024*1024:
                data = fi.read(int(readCfg['head']*1024*1024))
                cpos+= len(data)
            elif cpos>=(path.size - readCfg['tail']*1024*1024):
                data = fi.read(int(readCfg['tail']*1024*1024))
                cpos+= len(data)
            else:
                data = fi.read(int(readCfg['read']*1024*1024))
                cpos+= len(data)
                
            if not data:
                break
            
            hash.update(data)
            fi.seek(readCfg['skip']*1024*1024, os.SEEK_CUR)
        
        bases = Bases()
        return "FastContentHashV1,sz:%06s,hash:%s" % (bases.toBase62(path.size), hash.hexdigest())
   

