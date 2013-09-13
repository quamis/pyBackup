# -*- coding: utf-8 -*-

'''
Created on Sep 7, 2013

@author: lucian
'''
import sys, os
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
        
        self.fileComparer.setCacheXml(self.worklog.xml.find('files'))
    
    def _pre(self):
        print "Start scanner"
        
    def _post(self):
        print "\n\nWrite worklog" 
        self.worklog.close()
        print "Backup done"    
        
    def run(self):
        self._pre();
        
        print "Get filelist in the input folder"
        total = len(self.inputReader.getAll())
        
        for (status, index, p, pi, po, hi, ho) in self.getDifferentFiles():
            sys.stdout.write("\n%04.1f    [%- 10s] %- 100s" % (100*float(index)/total, status, p[0:100]))
            sys.stdout.flush()
            
            if status=="new":
                self.writer.addFile(pi, po)
                
            if status=="newdir":
                self.writer.addDir(po)

            if status=="old":
                self.writer.rmFile(po)
                
            if status=="olddir":
                self.writer.rmDir(po)
                
            if status=="changed":
                self.writer.updateFile(pi, po)
                
            self.worklog.append(p, hi, status)
        self._post();
        
    def _callback(self, index):
        pass
        
    def getDifferentFiles(self):
        print "Get filelist in the target folder"
        outputFiles = self.outputReader.getAll()
        
        print "Start comparer"
        index = 0
        for p in self.inputReader.read():
            index+= 1
            self._callback(index)
            
            pi = os.path.join(self.inputReader.base(), p)
            hi = None
            po = os.path.join(self.outputReader.base(), p)
            ho = None
            if os.path.isdir(pi):
                if p not in outputFiles:
                    yield ('newdir', index, p, pi, po, hi, ho)
                else:
                    yield ('dir', index, p, pi, po, hi, ho)
                    outputFiles.remove(p)
                continue
                
            hi = self.fileComparer.hash(pi, None)
            ho = None
            if p not in outputFiles:
                yield ('new', index, p, pi, po, hi, ho)
            else:
                ho = self.fileComparer.hash(po, p)
                
                if hi == ho:
                    yield ('file', index, p, pi, po, hi, ho)
                else:
                    yield ('changed', index, p, pi, po, hi, ho)
                
                outputFiles.remove(p)
            
        outputFiles.sort(reverse=True)
        for p in outputFiles:
            po = os.path.join(self.outputReader.base(), p)
            if os.path.isdir(po):
                yield ('olddir', index, p, None, po, None, None)
            else:
                ho = self.fileComparer.hash(po, p)
                yield ('old', index, p, None, po, None, ho)
            
            