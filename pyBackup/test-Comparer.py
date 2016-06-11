# -*- coding: utf-8 -*-
'''
@author: lucian
'''

import pprint
from Comparer.Comparer import Comparer
import Cache.sqlite as sqlite

pp = pprint.PrettyPrinter(indent=4)

cacheNew = sqlite.sqlite();
cacheNew.setCacheLocation('FileSystem.sqlite')

cacheOld = sqlite.sqlite();
cacheOld.setCacheLocation('FileSystem-old.sqlite')

cmpr = Comparer()
cmpr.setNewCache(cacheNew)
cmpr.setOldCache(cacheOld)
cmpr.initialize()


print "deleted files:"
pprint.pprint(cmpr.getAllNew())

print "moved files:"
pprint.pprint(cmpr.getAllMoved())

print "changed files:"
pprint.pprint(cmpr.getAllChanged())

print "new files:"
pprint.pprint(cmpr.getAllNew())

cmpr.destroy()
