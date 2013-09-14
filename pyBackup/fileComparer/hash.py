# -*- coding: utf-8 -*-
'''
Created on Sep 7, 2013

@author: lucian
'''
import os
import base
import hashlib

class hash(base.base):
    '''
    Compare 2 files by comparing their filesize
    '''

    def _hash(self, f):
        if self.exists(f):
            return "%s.%s.%s" % (
                 super(hash, self)._hash(f),
                 self.get_hexsize(f),
                 self.get_md5(f)
             )

    def get_md5(self, f):
        fi = open(f, 'rb')
        md5 = hashlib.md5()
        while True:
            data = fi.read(int(2.5*1024*1024))
            if not data:
                break
            md5.update(data)
            
        return md5.hexdigest()
   