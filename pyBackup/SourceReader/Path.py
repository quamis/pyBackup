class Path():
    def __init__(self, path, isDir):
        self.path = path
        self.isDir = isDir
        
        self.ctime = None
        self.mtime = None
        self.atime = None
        self.size = None

    def __repr__(self):
        return "%s%s" % (self.path, ("/" if self.isDir else ""))
    
    def initialize(self):
        pass
    