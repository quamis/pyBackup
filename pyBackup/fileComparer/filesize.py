'''
Created on Sep 7, 2013

@author: lucian
'''
import os

class filesize(object):
    '''
    Compare 2 files by comparing their filesize
    '''


    def __init__(self, options):
        '''
        Initialize the object
        '''
        self.options = options
        
    def getDifferences(self, input, output):
        raise "Not implemented"
        
    def isEqual(self, input, output):
        return os.path.getsize(input) == os.path.getsize(output)
    