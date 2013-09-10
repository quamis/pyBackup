'''
Created on Sep 7, 2013

@author: lucian
'''
import os
import base

class filesize(base.base):
    '''
    Compare 2 files by comparing their filesize
    '''

    def isEqual(self, input, output):
        if os.path.exists(input) and os.path.exists(output):
            return os.path.getsize(input) == os.path.getsize(output)
        
        return False
    