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


    def __init__(self, inputReader, outputReader, writer, fileComparer):
        '''
        Initialize object
        '''
        self.inputReader = inputReader
        self.outputReader = outputReader
        self.writer = writer
        self.fileComparer = fileComparer
        
        self.worklog = config.worklog.worklog(os.path.join(self.writer.base(), "worklog.xml"))
        
        
    def run(self):
        #print "\n".join(self.reader.getAll())
        
        for (status, p, pi, po, hi, ho) in self.getDifferentFiles():
            if status=="new":
                print "[%s] %s" % (status, p)
                self.writer.addFile(pi, po)
            
            """
            if status=="old":
                print "[%s] %s" % (status, p)
                self.writer.rmFile(po)
                
            if status=="changed":
                print "[%s] %s" % (status, p)
                self.writer.updateFile(pi, po)
            """
                
        self.worklog.close()
        
    def getDifferentFiles(self):
        outputFiles = self.outputReader.getAll()
        
        for p in self.inputReader.read():
            pi = os.path.join(self.inputReader.base(), p)
            hi = self.fileComparer.hash(pi)
            po = os.path.join(self.outputReader.base(), p)
            ho = None
            
            if p not in outputFiles:
                yield ('new', p, pi, po, hi, ho)
            else:
                po = os.path.join(self.outputReader.base(), p)
                ho = self.fileComparer.hash(po)
                
                if hi == ho:
                    yield ('identical', p, pi, po, hi, ho)
                else:
                    yield ('changed', p, pi, po, hi, ho)
                
                outputFiles.remove(p)
            
        for p in outputFiles:
            po = os.path.join(self.outputReader.base(), p)
            ho = self.fileComparer.hash(po)
            yield ('old', p, None, po, None, ho)
            