import os, shutil
import logging

class Writer(object):
    def __init__(self, backupBasePath, sourceBackupBasePath, id):
        self.backupBasePath = backupBasePath
        self.sourceBackupBasePath = sourceBackupBasePath
        self.id = id
    
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
    
    def updateFile(self, opath, npath):
        print "updateFile"
        
    def deleteFile(self, op):
        print "deleteFile"
            
