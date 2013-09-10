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

    def hash(self, file):
        if self.exists(file):
            return super(hash, self).hash(file) + self.get_md5(file)


    def get_md5(self, file):
        f = open(file, 'rb')
        md5 = hashlib.md5()
        while True:
            data = f.read(1024*1024)
            if not data:
                break
            md5.update(data)
            
        return md5.hexdigest()