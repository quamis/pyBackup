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

    def getDestinationFilePathToContent(self, p):
        return p
    
    def registerProgressCallback(self, callback):
        self.progressCallback = callback
        
        
    def moveFile(self, opath, npath):
        opath2 = opath.path.replace(self.sourceBasePath, '', 1)
        npath2 = npath.path.replace(self.sourceBasePath, '', 1)
        
        self.mkdir(self.backupBasePath+npath2)
        shutil.move(self.backupBasePath+opath2, self.backupBasePath+npath2)
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'moveFile', {'path':opath, 'isDir':False})
        
    def updateFile(self, opath, npath):
        npath2 = npath.path.replace(self.sourceBasePath, '', 1)
        shutil.copyfile(npath.path, self.backupBasePath+npath2)
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'updateFile', {'path':opath, 'isDir':False})
        
    def newFile(self, npath):
        npath2 = npath.path.replace(self.sourceBasePath, '', 1)
        
        self.mkdir(self.backupBasePath+npath2)
        shutil.copyfile(npath.path, self.backupBasePath+npath2)
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'newFile', {'path':npath, 'isDir':False})

        
    def newDir(self, npath):
        npath2 = npath.path.replace(self.sourceBasePath, '', 1)
        if not os.path.isdir(self.backupBasePath+npath2):
            os.mkdir(self.backupBasePath+npath2)
            
        if not self.progressCallback is None:
            self.progressCallback(self, 'newDir', {'path':npath, 'isDir':True})
        
    
    def deleteFile(self, opath):
        opath2 = opath.path.replace(self.sourceBasePath, '', 1)
        os.unlink(self.backupBasePath+opath2)
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'deleteFile', {'path':opath, 'isDir':False})
            
        
    def deleteDir(self, opath):
        opath2 = opath.path.replace(self.sourceBasePath, '', 1)
        os.rmdir(self.backupBasePath+opath2)
        
        if not self.progressCallback is None:
            self.progressCallback(self, 'deleteDir', {'path':opath, 'isDir':True})
        
    def mkdir(self, fpath):
        dname = os.path.dirname(fpath)+'/'
        if not os.path.isdir(dname):
            os.makedirs(dname)
            