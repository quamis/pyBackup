# -*- coding: utf-8 -*-

'''
Created on Sep 7, 2013

@author: lucian
'''
import os, errno

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
        self.stats = {
          'addFile': {
            'count': 0,
            'size': 0,
          },
          'rmFile': {
            'count': 0,
            'size': 0,
          },
          'updateFile': {
            'count': 0,
            'size': 0,
            'dsize': 0,
          },
        }
        
    def getStats(self):
        return self.stats
    
    def base(self):
        return self.path
    
    def addFile(self, input, output):
        self.stats['addFile']['count']+=1
        self.stats['addFile']['size']+=os.path.getsize(input)
        self._mkdir(os.path.dirname(output))
        self._copyFile(input, output)
        
        
    def addDir(self, output):
        self._mkdir(os.path.dirname(output))
        
    def updateFile(self, input, output):
        self.stats['updateFile']['count']+=1
        self.stats['updateFile']['size']+=os.path.getsize(input)
        self.stats['updateFile']['dsize']+=os.path.getsize(output) - os.path.getsize(input)
        self._copyFile(input, output)
        
    def rmFile(self, output):
        self.stats['rmFile']['count']+=1
        self.stats['rmFile']['size']+=os.path.getsize(output)
        self._rmFile(output)
        
    def rmDir(self, output):
        self._rmDir(output)
    
    def _rmFile(self, file, progress_callback=None):
        os.unlink(file)
        
    def _rmDir(self, output, progress_callback=None):
        os.rmdir(output)
        
    def _copyFile(self, input, output, progress_callback=None):
        source = open(input, 'rb')
        dest = open(output, 'wb')
        
        bufferSize = (int)(2.5*1024*1024);
        
        pos = 0
        while 1:
            buffer = source.read(bufferSize)
            if buffer:
                pos+=len(buffer)
                if progress_callback is not None:
                    progress_callback(pos)
                dest.write(buffer)
            else:
                break
        
        source.close()
        dest.close()
        
    
    def _mkdir(self, path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
            