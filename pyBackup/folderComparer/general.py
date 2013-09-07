'''
Created on Sep 7, 2013

@author: lucian
'''

class general(object):
    '''
    General folder comparer
    '''


    def __init__(self, options):
        '''
        Initialize the object
        '''
        self.options = options
        
    def isEqual(self, input, output):
        return False