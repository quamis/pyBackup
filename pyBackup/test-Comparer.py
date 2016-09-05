# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import pprint
from Comparer.SimpleComparer import SimpleComparer
from Comparer.CompleteComparer import CompleteComparer
import Cache.sqlite as sqlite

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cacheNew',  dest='cacheNew',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--cacheOld',  dest='cacheOld', action='store', type=str,   default='',help='TODO')
args = vars(parser.parse_args())


cacheNew = sqlite.sqlite();
cacheNew.setCacheLocation(args['cacheNew'])

cacheOld = sqlite.sqlite();
cacheOld.setCacheLocation(args['cacheOld'])

#doApply = True
#cmpr = SimpleComparer()
doApply = False
cmpr = CompleteComparer()

cmpr.setNewCache(cacheNew)
cmpr.setOldCache(cacheOld)
cmpr.initialize()



"""
    TODO: 
        - correctly handle moved file vs delete+new file
"""

print "moved files:"
for paths in cmpr.getAllMoved():
    print "    ren %s --> %s" % (paths[1], paths[0])

    if doApply:
        cmpr.movePath(paths[1], paths[0])
        print "    ...marked"
cmpr.commit()


print "deleted files:"
# TODO: do some sort of backups
for paths in cmpr.getAllDeleted():
    print "    del %s" % (paths[0])
    
    if doApply:
        cmpr.deletePath(paths[0])
        print "    ...deleted"
cmpr.commit()


print "changed files:"
# TODO: do some sort of backups
for paths in cmpr.getAllChanged():
    print "    upd %s --> %s" % (paths[1], paths[0], )

    if doApply:
        cmpr.updatePath(paths[1], paths[0])
        print "    ...updated"
cmpr.commit()


print "new files:"
for paths in cmpr.getAllNew():
    print "    cpy %s" % (paths[0], )

    if doApply:
        cmpr.newPath(paths[0])
        print "    ...copied"
cmpr.commit()


cmpr.destroy()

