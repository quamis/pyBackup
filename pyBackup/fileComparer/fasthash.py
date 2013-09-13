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
    Compare 2 files by comparing their filesize
    '''

    def _hash(self, f):
        if self.exists(f):
            return "%s.%s.%s" % (
                 super(fasthash, self)._hash(f),
                 self.get_hexsize(f),
                 self.get_md5_sparse(f)
                 )

    def get_md5_sparse(self, f):
        """
        calculate the md5 hash for a file, by reading sparse cheunks o \f data from it.
        Very fast compared to the direct approach, but error-prone, it may lead to false-positives(it may consider 2 files as equal, even if they aren't 
        """
        
        # a list of "linear files". Basically this are files on which we shouldn't use the "sparse" scan method 
        if f.lower().endswith(('.txt', '.csv', '.img', 'db', '.sqlite')):
            read_chunk = int(2*1024*1024)
            skip_chunk = int(0*1024*1024)
        else:
            size = float(os.path.getsize(f))/(1024*1024*1024)
            
            if size<0.25:
                read_chunk = int(2*1024*1024)
                skip_chunk = int(0*1024*1024)
            elif size<0.8:
                read_chunk = int(2*1024*1024)
                skip_chunk = int(1*1024*1024)
            elif size<2.0:
                read_chunk = int(2*1024*1024)
                skip_chunk = int(2*1024*1024)
            elif size<4.0:
                read_chunk = int(2*1024*1024)
                skip_chunk = int(4*1024*1024)
            elif size<8.0:
                read_chunk = int(2*1024*1024)
                skip_chunk = int(8*1024*1024)
            else:
                read_chunk = int(2*1024*1024)
                skip_chunk = int(16*1024*1024)
        
        fi = open(f, 'rb')
        md5 = hashlib.md5()
        while True:
            data = fi.read(read_chunk)
            if not data:
                break
            md5.update(data)
            
            fi.seek(skip_chunk, os.SEEK_CUR)
            
        return md5.hexdigest()