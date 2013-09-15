# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013

@author: lucian
'''
import os
import hash
import hashlib

class fasthash(hash.hash):
    '''
    Compare 2 files by comparing their hashes, in an error-prone but really fast way
    '''
    def init(self):
        self.stats['calls_cached'] = 0
        self.stats['calls_real'] = 0
        self.stats['_h_md5_sparse_type'] = {
            (2, 0.00):   0,
            (2, 0.25):   0,
            (2, 0.50):   0,
            (2, 0.75):   0,
            (1, 1.25):   0,
            (2, 2):      0,
            (2, 4):      0,
            (2, 8):      0,
            (2, 16):     0,
        }
    
    
    def hash(self, absf, dt, dsrc):
        if self.cache and self.options['cache_enabled'] and self.cache.exists(dt['p']):
            if self.options['cache_use_hints'] and dsrc=='i':
                ch = self.cache.get(dt['p'])
                if dt['imtime']==ch['mtime'] and dt['isize']==ch['size'] :
                    self.stats['calls_cached']+=1
                    return self.cache.getHash(dt['p'])
            if dsrc=='o':
                self.stats['calls_cached']+=1
                return self.cache.getHash(dt['p'])
        
        self.stats['calls_real']+=1
        return self._hash(absf)
    
    def _hash(self, f):
        if self.exists(f):
            return "%s.%s.%s" % (
                 self._h_exists(f),
                 self._h_hexsize(f),
                 self._h_md5_sparse(f)
             )
            
    def _h_md5_sparse(self, f):
        """
        calculate the md5 hash for a file, by reading sparse cheunks o \f data from it.
        Very fast compared to the direct approach, but error-prone, it may lead to false-positives(it may consider 2 files as equal, even if they aren't 
        """
        
        # a list of "linear files". Basically this are files on which we shouldn't use the "sparse" scan method 
        if f.lower().endswith(('.txt', '.csv', '.img', 'db', '.sqlite')):
            read_chunk = 2
            skip_chunk = 0
        else:
            size = float(os.path.getsize(f))/(1024*1024*1024)
            
            if size<0.02:   # 20Mb
                read_chunk = 2
                skip_chunk = 0
            elif size<0.10:   # 100Mb
                read_chunk = 2
                skip_chunk = 0.25
            elif size<0.20:   # 200Mb
                read_chunk = 2
                skip_chunk = 0.5
            elif size<0.25:
                read_chunk = 2
                skip_chunk = 0.75
            elif size<1.0:
                read_chunk = 2
                skip_chunk = 1
            elif size<2.0:
                read_chunk = 2
                skip_chunk = 2
            elif size<4.0:
                read_chunk = 2
                skip_chunk = 4
            elif size<8.0:
                read_chunk = 2
                skip_chunk = 8
            else:
                read_chunk = 2
                skip_chunk = 16
        
        self.stats['_h_md5_sparse_type'][(read_chunk, skip_chunk)]+=1
        
        read_chunk = int(read_chunk*1024*1024)
        skip_chunk = int(skip_chunk*1024*1024)
        
        fi = open(f, 'rb')
        md5 = hashlib.md5()
        while True:
            data = fi.read(read_chunk)
            if not data:
                break
            md5.update(data)
            
            fi.seek(skip_chunk, os.SEEK_CUR)
            
        return md5.hexdigest()