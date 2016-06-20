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
        
    def hash(self, path):
        hasherMapByExtenstion = [
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

        stats = {
            'head_cnt':0,
            'head_sz': 0,
            'tail_cnt':0,
            'tail_sz': 0,
            'data_cnt':0,
            'data_sz': 0,
        }


        cpos = 0
        while True:
            if readCfg['head'] and cpos<=readCfg['head']*1024*1024:
                data = fi.read(int(readCfg['head']*1024*1024))
                dl = len(data)
                cpos+= dl
                stats['head_cnt']+= 1
                stats['head_sz']+=  dl
            elif readCfg['tail'] and cpos>=(path.size - (readCfg['skip']*1024*1024) - (readCfg['tail']*1024*1024)):
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
            
            hash.update(data)
            if readCfg['skip']:
                fi.seek(readCfg['skip']*1024*1024, os.SEEK_CUR)
                cpos+=readCfg['skip']*1024*1024
        

        bases = Bases()
        return "FastContentHashV1,sz:%06s,hash:%s" % (bases.toBase62(path.size), hash.hexdigest())
   

