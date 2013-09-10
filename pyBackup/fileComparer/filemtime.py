'''
Created on Sep 7, 2013

@author: lucian
'''
import os
import base

class filemtime(base.base):
    '''
    Compare 2 files by comparing their filesize
    '''

    def hash(self, file):
        if self.exists(file):
            return super(filemtime, self).hash(file) + str(os.path.getmtime(file))
