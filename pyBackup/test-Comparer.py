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

print "moved files:"
for paths in cmpr.getAllMoved():
    print "    %s --> %s" % (paths[1], paths[0])
    
    cmpr.movePath(paths[1], paths[0])
    print "    ...marked"
    


"""
print "deleted files:"
for paths in cmpr.getAllNew():
    # TODO: do some sort of backups
    print paths[0]


print "changed files:"
# TODO: do some sort of backups
pprint.pprint(cmpr.getAllChanged())

print "new files:"
pprint.pprint(cmpr.getAllNew())
"""

cmpr.destroy()
