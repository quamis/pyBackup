# -*- coding: utf-8 -*-
'''
@author: lucian
'''

import pprint
from SourceReader.LocalPathReader import LocalPathReaderCached
from SourceReader.LocalPathReader import LocalPathReader
from Hasher.FastHashV1 import FastHashV1
from Hasher.FastHashV1 import FastHashV1Cached
import Cache.sqlite as sqlite

pp = pprint.PrettyPrinter(indent=4)

DB = 'FileSystem.sqlite'
cache = sqlite.sqlite();
cache.setCacheLocation(DB)

lp = LocalPathReaderCached.LocalPathReaderCached()
lp.setCache(cache)
#lp = LocalPathReader.LocalPathReader()
lp.setPath('/tmp/x/')
lp.initialize()


hh = FastHashV1Cached.FastHashV1Cached()
hh.setCache(cache)
hh.initialize()

print "-"*80
for p in iter(lambda:lp.getNext(), None):
    print p.path
    if not p.isDir:
	print "    "+hh.hash(p)
print "-"*80

lp.destroy()
hh.destroy()
