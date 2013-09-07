'''
Created on Sep 7, 2013

@author: lucian
'''

class copy(object):
    '''
    Writer module to directly copy data to a certain location
    '''


    def __init__(self, path, options):
        '''
        Initialize the writer
        '''
        self.path = path
        self.options = options