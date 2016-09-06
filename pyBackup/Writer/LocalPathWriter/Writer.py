import os, shutil

class Writer(object):
    def __init__(self, backupBasePath, sourceBasePath):
        self.backupBasePath = backupBasePath
        self.sourceBasePath = sourceBasePath
    
    def initialize(self):
        print "writer initialize"
    
    def destroy(self):
        self.commit()
        
    def commit(self):
        pass
        
        
    def moveFile(self, opath, npath):
        opath2 = opath.replace(self.sourceBasePath, '', 1)
        npath2 = npath.replace(self.sourceBasePath, '', 1)
        
        self.mkdir(self.backupBasePath+npath2)
        shutil.move(self.backupBasePath+opath2, self.backupBasePath+npath2)
        
    def updateFile(self, opath, npath):
        npath2 = npath.replace(self.sourceBasePath, '', 1)
        shutil.copy(npath, self.backupBasePath+npath2)
        
    def newFile(self, npath):
        npath2 = npath.replace(self.sourceBasePath, '', 1)
        shutil.copy(npath, self.backupBasePath+npath2)
        
    def newDir(self, npath):
        npath2 = npath.replace(self.sourceBasePath, '', 1)
        if not os.path.isdir(self.backupBasePath+npath2):
            os.mkdir(self.backupBasePath+npath2)
        
    
    def deleteFile(self, opath):
        opath2 = opath.replace(self.sourceBasePath, '', 1)
        os.unlink(self.backupBasePath+opath2)
        
    def deleteDir(self, opath):
        opath2 = opath.replace(self.sourceBasePath, '', 1)
        os.rmdir(self.backupBasePath+opath2)
        
        
    def mkdir(self, fpath):
        if not os.path.isdir(os.path.dirname(fpath)+'/'):
            os.makedirs(os.path.dirname(fpath+'/'))