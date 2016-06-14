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
    print "    ren %s --> %s" % (paths[1], paths[0])
    
    #cmpr.movePath(paths[1], paths[0])
    #print "    ...marked"
cmpr.commit()

"""
print "deleted files:"
# TODO: do some sort of backups
for paths in cmpr.getAllDeleted():
    print "    del %s" % (paths[0])
    
    cmpr.deletePath(paths[0])
    print "    ...deleted"
cmpr.commit()


print "changed files:"
# TODO: do some sort of backups
for paths in cmpr.getAllChanged():
    print "    upd %s --> %s" % (paths[1], paths[0], )
    
    cmpr.updatePath(paths[1], paths[0])
    print "    ...updated"
cmpr.commit()


print "new files:"
for paths in cmpr.getAllNew():
    print "    cpy %s" % (paths[0], )
    
    cmpr.newPath(paths[0])
    print "    ...copied"
cmpr.commit()
"""


cmpr.destroy()
