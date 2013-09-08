'''
Created on Sep 7, 2013

@author: lucian
'''

class general(object):
    '''
    General folder comparer
    '''


    def __init__(self, fileComparer, options):
        '''
        Initialize the object
        '''
        self.fileComparer = fileComparer
        self.options = options
        
    def isEqual(self, input, output):
        return False