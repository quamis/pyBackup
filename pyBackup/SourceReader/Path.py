class Path():
    def __init__(self, path, isDir):
        self.path = path
        self.isDir = isDir

    def __repr__(self):
        return "%s%s" % (self.path, ("/" if self.isDir else ""))
