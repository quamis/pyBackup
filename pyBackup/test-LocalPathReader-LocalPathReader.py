import pprint
from SourceReader.LocalPathReader import LocalPathReader

pp = pprint.PrettyPrinter(indent=4)

lp = LocalPathReader.LocalPathReader()
lp.setPath("/tmp/x/")
lp.initialize()


for p in iter(lambda:lp.getNext(), None):
    #pp.pprint([p.path, p.isDir])
    pp.pprint(p)


