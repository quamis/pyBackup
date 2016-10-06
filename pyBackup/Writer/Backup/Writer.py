import os, shutil
import logging

class Writer(object):
    def __init__(self, backupBasePath, sourceBackupBasePath, sourceSourceBasePath, id):
        self.backupBasePath = backupBasePath
        self.sourceBackupBasePath = sourceBackupBasePath
        self.sourceSourceBasePath = sourceSourceBasePath
        self.id = id
    
    def initialize(self):
        logging.info("writer initialize")
    
    def destroy(self):
        self.commit()
        
    def commit(self):
        pass
    
    def getFilePathInSource(self, npath):
        return "%s%s/%s" % (self.backupBasePath, self.id, npath.replace(self.sourceSourceBasePath, '', 1))
        
    def getFilePathInBackup(self, npath):
        return self.sourceBackupBasePath + npath.replace(self.sourceSourceBasePath, '', 1)

    def getDestinationFilePathToContent(self, p):
        return p
    
    def updateFile(self, opath, npath):
        dst = self.getFilePathInSource(npath.path)
        src = self.getFilePathInBackup(npath.path)
        
        self.mkdir(dst)
        shutil.copyfile(src, dst)
        
    def deleteFile(self, opath):
        dst = self.getFilePathInSource(opath.path)
        src = self.getFilePathInBackup(opath.path)
        
        self.mkdir(dst)
        shutil.copyfile(src, dst)
        
    def mkdir(self, fpath):
        dname = os.path.dirname(fpath)+'/'
        if not os.path.isdir(dname):
            os.makedirs(dname)
            