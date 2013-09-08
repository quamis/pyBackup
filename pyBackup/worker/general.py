'''
Created on Sep 7, 2013

@author: lucian
'''
import os;

class general(object):
    '''
    Basic backup processor
    '''


    def __init__(self, reader, writer, fileComparer):
        '''
        Initialize object
        '''
        self.reader = reader
        self.writer = writer
        self.fileComparer = fileComparer
        
        
    def run(self):
        #print "\n".join(self.reader.getAll())
        
        for p in self.reader.read():
            pi = os.path.join(self.reader.base(), p)
            po = os.path.join(self.writer.base(), p)
            
            if not self.fileComparer.isEqual(pi, po):
                print "%s , %s" % (pi, po)
                print "diff"
                
                self.writer.copy(pi, po)
                
            else:
                print "eq"
                
        