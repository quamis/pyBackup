class PathFormatter(object):
    def __init__(self, maxLength):
        self.maxLength = maxLength
    
    def format(self, p):
        o = u""
        p = p.encode("utf-8")
        
        if len(p)>self.maxLength:
            o = "%s...%s" % (p[0:50], p[-(self.maxLength-50-3):])
        else:
            o = "%s" % (p)
        return o

