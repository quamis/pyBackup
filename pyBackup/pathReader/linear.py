'''
Created on Sep 7, 2013

@author: lucian
'''
import os, sys, fnmatch;

class linear(object):
    '''
    Read a path(file) and return it directly
    '''


    def __init__(self, path, options):
        '''
        Initialize the parser
        '''
        self.path = path
        self.options = options
        
    def getAll(self):
        return [self.path]
