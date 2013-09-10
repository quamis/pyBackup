'''
Created on Sep 8, 2013

@author: lucian
'''
import os

class base(object):
    '''
    Base class that all other comparison modules should extends
    '''


    def __init__(self, options):
        '''
        Initialize the class
        '''
        self.options = options
        
    def getDifferences(self, input, output):
        raise "Not implemented"
        
    def exists(self, file):
        return os.path.exists(file)
    
    def hash(self, file):
        return "E" if self.exists(file) else "N"
