'''
Created on Sep 7, 2013

@author: lucian
'''
import os
import config.worklog


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
        
        self.worklog = config.worklog.worklog(os.path.join(self.writer.base(), "worklog.xml"))
        
        
    def run(self):
        #print "\n".join(self.reader.getAll())
        
        for p in self.reader.read():
            pi = os.path.join(self.reader.base(), p)
            po = os.path.join(self.writer.base(), p)
            
            hi = self.fileComparer.hash(pi)
            ho = self.fileComparer.hash(po)
            
            if hi != ho:
                print "%s" % (pi)
                self.writer.copy(pi, po)
                self.worklog.append(pi, hi)
            else:
                #print "eq"
                pass
                
        self.worklog.close()