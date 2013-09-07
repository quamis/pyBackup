'''
Created on Sep 7, 2013

@author: lucian
'''

class general(object):
    '''
    Basic backup processor
    '''


    def __init__(self, reader, writer, folderComparer, fileComparer):
        '''
        Initialize object
        '''
        self.reader = reader
        self.writer = writer
        self.folderComparer = folderComparer
        self.fileComparer = fileComparer
        
        
    def run(self):
        print self.reader.getAll()