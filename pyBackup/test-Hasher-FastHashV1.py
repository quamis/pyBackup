import pprint
from SourceReader.LocalPathReader import LocalPathReader
from Hasher.FastHashV1 import FastHashV1
from Hasher.FastHashV1 import FastHashV1Cached

pp = pprint.PrettyPrinter(indent=4)

lp = LocalPathReader.LocalPathReader()
lp.setPath("/tmp/x/")
lp.initialize()


hh = FastHashV1.FastHashV1()
hh.initialize()

for p in iter(lambda:lp.getNext(), None):
    print p.path
    if not p.isDir:
	print "    "+hh.hash(p)


lp.destroy()
hh.destroy()
