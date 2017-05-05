import os, shutil
import logging

class Writer(object):
    def __init__(self, backupBasePath, sourceBasePath):
        self.backupBasePath = backupBasePath
        self.sourceBasePath = sourceBasePath
        self.progressCallback = None
    
    def initialize(self):
        logging.info("writer initialize")
    
    def destroy(self):
        self.commit()
        
    def commit(self):
        pass
        
    def getDestinationFilePath(self, npath):
        return self.backupBasePath + npath.replace(self.sourceBasePath, '', 1)
        
    def getSourceFilePath(self, npath):
        return self.sourceBasePath + npath.replace(self.backupBasePath, '', 1)

    def getDestinationFilePathToContent(self, p):
        return p
    
    def registerProgressCallback(self, callback):
        self.progressCallback = callback
        
        
    def moveFile(self, opath, npath):
        self.mkdir(self.getDestinationFilePath(npath.path))
        shutil.move(self.getDestinationFilePath(opath.path), self.getDestinationFilePath(npath.path))
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'moveFile', {'path':opath, 'isDir':False})
        
    def updateFile(self, opath, npath):
        shutil.copyfile(npath.path, self.getDestinationFilePath(npath.path))
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'updateFile', {'path':opath, 'isDir':False})
        
    def newFile(self, npath):
        self.mkdir(self.getDestinationFilePath(npath.path))
        shutil.copyfile(npath.path, self.getDestinationFilePath(npath.path))
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'newFile', {'path':npath, 'isDir':False})

        
    def newDir(self, npath):
        if not os.path.isdir(self.getDestinationFilePath(npath.path)):
            os.mkdir(self.getDestinationFilePath(npath.path))
            
        if not self.progressCallback is None:
            self.progressCallback(self, 'newDir', {'path':npath, 'isDir':True})
    
    def deleteFile(self, opath):
        os.unlink(self.getDestinationFilePath(opath.path))
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'deleteFile', {'path':opath, 'isDir':False})
            
        
    def deleteDir(self, opath):
        os.rmdir(self.getDestinationFilePath(opath.path))
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'deleteDir', {'path':opath, 'isDir':True})
        
    def mkdir(self, fpath):
        dname = os.path.dirname(fpath)+'/'
        if not os.path.isdir(dname):
            os.makedirs(dname)
            