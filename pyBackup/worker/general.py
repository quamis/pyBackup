# -*- coding: utf-8 -*-

'''
Created on Sep 7, 2013

@author: lucian
'''
import sys, os
import config.worklog
import config.cache


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
        
        self.worklog =  config.worklog.worklog(os.path.join(self.writer.base(), "_pyBackup.xml"))
        self.cache =    config.cache.cache(os.path.join(self.writer.base(), "_pyBackup.cache.xml"))
        
        self.inputFiles =    None
        self.outputFiles =    None
        
        self.fileComparer.setCacheXml(self.cache)
    
    def _pre(self):
        print "Start scanner"
        print "Open cache"
        self.cache.open()
        
        print "Get filelist in the input folder"
        self.inputFiles = self.inputReader.getAll()
        
        print "Get filelist in the target folder"
        self.outputFiles = self.outputReader.getAll()
        
    def _post(self):
        print "\n\nWrite worklog" 
        self.worklog.close()
        print "Write cache"
        self.cache.close()
        print "Backup done"    
        
    def run(self):
        self._pre();
        
        print "Get filelist in the input folder"
        totalFiles = len(set(self.inputFiles + self.outputFiles))
        
        printType = None
        for (status, index, p, dt) in self.getDifferentFiles():
            if status in ('file', 'dir'):
                if printType=="n":
                    sys.stdout.write("\n")
                
                sys.stdout.write("\r%04.1f    [%- 10s] %- 100s" % (100*float(index)/totalFiles, status, p[0:100]))
                sys.stdout.flush()
                printType = "o"
            else:
                if printType=="o":
                    sys.stdout.write("\r")
                else:
                    sys.stdout.write("\n")
                    
                sys.stdout.write("%04.1f    [%- 10s] %- 100s" % (100*float(index)/totalFiles, status, p[0:100]))
                sys.stdout.flush()
                printType = "n"
                
            if status=="new":
                self.writer.addFile(dt['pi'], dt['po'])
                
            if status=="newdir":
                self.writer.addDir(dt['po'])

            if status=="old":
                self.writer.rmFile(dt['po'])
                
            if status=="olddir":
                self.writer.rmDir(dt['po'])
                
            if status=="changed":
                self.writer.updateFile(dt['pi'], dt['po'])
                
            
            self.cache.set(p, {
               'status':    status,
               'hash':      dt['hi'], 
               'size':      dt['isize'],
               'mtime':     dt['imtime'],
               })
        self._post();
        
    def _callback(self, index):
        pass
        
    def getDifferentFiles(self):
        print "Start comparer"
        index = 0
        
        outputFiles = self.outputFiles
        
        for p in self.inputFiles:
            index+= 1
            self._callback(index)
            
            dt = {
                'p': p,
                'pi': None, 'po': None, 'hi': None, 'ho': None,
                'isize': None, 'imtime': None,
                'osize': None, 'omtime': None,
            }
            dt['p'] =  p
            dt['pi'] = os.path.join(self.inputReader.base(), p)
            dt['po'] = os.path.join(self.outputReader.base(), p)
            
            if os.path.isdir(dt['pi']):
                if p not in outputFiles:
                    yield ('newdir', index, p, dt)
                else:
                    yield ('dir', index, p, dt)
                    outputFiles.remove(p)
                continue
            
            try:
                dt['isize'] =   os.path.getsize(dt['pi'])
                dt['imtime'] =  os.path.getmtime(dt['pi'])
            except OSError:
                print "File went missing %s" % ( p )
                continue
                
            dt['hi'] = self.fileComparer.hash(dt['pi'], dt, 'i')
            dt['ho'] = None
            if p not in outputFiles:
                yield ('new', index, p, dt)
            else:
                try:
                    dt['osize'] =   os.path.getsize(dt['po'])
                    dt['omtime'] =  os.path.getmtime(dt['po'])
                except OSError:
                    print "File went missing %s" % ( p )
                    continue
            
                dt['ho'] = self.fileComparer.hash(dt['po'], dt, 'o')
                
                if dt['hi'] == dt['ho']:
                    yield ('file', index, p, dt)
                else:
                    yield ('changed', index, p, dt)
                
                outputFiles.remove(p)
            
        outputFiles.sort(reverse=True)
        for p in outputFiles:
            index+= 1
            dt = {
                'p': p,
                'pi': None, 'po': None, 'hi': None, 'ho': None, 
                'isize': None, 'imtime': None,
                'osize': None, 'omtime': None,
            }
            dt['po']= os.path.join(self.outputReader.base(), p)
            if os.path.isdir(dt['po']):
                yield ('olddir', index, p, dt)
            else:
                yield ('old', index, p, dt)
            
            