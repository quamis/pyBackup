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
        self.options = {
            'cache_enabled': True if ('cache_enabled' in options and options['cache_enabled']) else False,
            'cache_use_hints': True if ('cache_use_hints' in options and options['cache_use_hints']) else False,
        }
        self.cache = None
        
    def getDifferences(self, input, output):
        raise "Not implemented"
        
    def exists(self, file):
        return os.path.exists(file)
    
    def hash(self, absf, dt, dsrc):
        return self._hash(absf)
    
    def _hash(self, absf):
        return self._h_exists(self, absf)
    
    def _h_exists(self, absf):
        return "E" if self.exists(absf) else "N"

    def _h_hexsize(self, f):
        return "%x" % (os.path.getsize(f))
    
    def setCacheXml(self, cache):
        self.cache = cache
            
