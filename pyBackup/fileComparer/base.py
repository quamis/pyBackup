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
        self.cacheData = None
        
    def getDifferences(self, input, output):
        raise "Not implemented"
        
    def exists(self, file):
        return os.path.exists(file)
    
    def hash(self, absf, relf):
        if self.cacheData and relf and relf in self.cacheData:
            return self.cacheData[relf]['hash']
        
        return self._hash(absf)
    
    def _hash(self, absf):
        return "E" if self.exists(absf) else "N"

    def setCacheXml(self, root):
        self.cacheData = {}
        for tag in root.findall("./file"):
            self.cacheData[tag.text] = tag.attrib
            
