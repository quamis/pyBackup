import pprint
from SourceReader.LocalPathReader import LocalPathReader

pp = pprint.PrettyPrinter(indent=4)

lp = LocalPathReader.LocalPathReader()
lp.setPath("test-data/data-m/")
lp.initialize()


for p in iter(lambda:lp.getNext(), None):
    #pp.pprint([p.path, p.isDir])
    pp.pprint(p)


lp.destroy()
