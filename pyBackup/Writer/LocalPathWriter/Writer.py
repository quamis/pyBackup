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
        
        
    def movePath(self, opath, npath):
        opath2 = opath.replace(self.sourceBasePath, '', 1)
        npath2 = npath.replace(self.sourceBasePath, '', 1)
        
        self.mkdir(self.backupBasePath+npath2)
        shutil.move(self.backupBasePath+opath2, self.backupBasePath+npath2)
        
    def updatePath(self, opath, npath):
        npath2 = npath.replace(self.sourceBasePath, '', 1)
        shutil.copy(npath, self.backupBasePath+npath2)
        
    def newPath(self, npath):
        npath2 = npath.replace(self.sourceBasePath, '', 1)
        shutil.copy(npath, self.backupBasePath+npath2)
    
    def deletePath(self, opath):
        opath2 = opath.replace(self.sourceBasePath, '', 1)
        os.unlink(self.backupBasePath+opath2)
        
        
    def mkdir(self, fpath):
        if not os.path.isdir(os.path.dirname(fpath)+'/'):
            os.makedirs(os.path.dirname(fpath+'/'))