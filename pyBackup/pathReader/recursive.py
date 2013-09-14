'''
Created on Sep 7, 2013

@author: lucian
'''
import os, sys, fnmatch;

class recursive(object):
    '''
    Recurse through a folder and return file-by-file
    '''


    def __init__(self, path, options):
        '''
        Initialize the parser
        '''
        self.path = path
        self.options = options
        
    def base(self):
        return self.path
        
    def getAll(self):
        paths = []
        for root, dirs, files in os.walk(self.path):
            for basename in files:
                if fnmatch.fnmatch(basename, "*"):
                    filename = os.path.join(root, basename)[len(self.path):]
                    paths.append(filename)
                    
            for basename in dirs:
                if fnmatch.fnmatch(basename, "*"):
                    filename = os.path.join(root, basename)[len(self.path):] + "/"
                    paths.append(filename)
                    
        return paths
