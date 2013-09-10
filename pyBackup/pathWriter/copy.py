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
    
    def base(self):
        return self.path
    
    def addFile(self, input, output):
        self._mkdir(os.path.dirname(output))
        self._copyFile(input, output)
        
    def updateFile(self, input, output):
        self._copyFile(input, output)
        
    def rmFile(self, output):
        self._rmFile(file)
    
    def _rmFile(self, file, progress_callback=None):
        os.unlink(file)
        if progress_callback is not None:
            progress_callback(1)
        
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
            