# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import pprint
from Comparer.CompleteComparer import CompleteComparer
from Writer.LocalPathWriter.Writer import Writer
import Cache.sqlite as sqlite

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cacheNew',  dest='cacheNew',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--cacheOld',  dest='cacheOld', action='store', type=str,   default='',help='TODO')
parser.add_argument('--source',  dest='source', action='store', type=str,   default='',help='TODO')
parser.add_argument('--backup',  dest='backup', action='store', type=str,   default='',help='TODO')
args = vars(parser.parse_args())


cacheNew = sqlite.sqlite();
cacheNew.setCacheLocation(args['cacheNew'])

cacheOld = sqlite.sqlite();
cacheOld.setCacheLocation(args['cacheOld'])

doApply = True
cmpr = CompleteComparer()

cmpr.setNewCache(cacheNew)
cmpr.setOldCache(cacheOld)
cmpr.initialize()

wrt = Writer(args['backup'], args['source'])
wrt.initialize()



print "moved files:"
for paths in cmpr.getAllMoved():
    print "    ren %s --> %s" % (paths[1], paths[0])

    if doApply:
        cmpr.movePath(paths[1], paths[0])
        wrt.movePath(paths[1], paths[0])
        print "    ...marked & applied"
cmpr.commit()
wrt.commit()


print "deleted files:"
# TODO: do some sort of backups
for paths in cmpr.getAllDeleted():
    print "    del %s" % (paths[0])
    
    if doApply:
        cmpr.deletePath(paths[0])
        wrt.deletePath(paths[0])
        print "    ...deleted & applied"
cmpr.commit()
wrt.commit()

print "changed files:"
# TODO: do some sort of backups
for paths in cmpr.getAllChanged():
    print "    upd %s --> %s" % (paths[1], paths[0], )

    if doApply:
        cmpr.updatePath(paths[1], paths[0])
        wrt.updatePath(paths[1], paths[0])
        print "    ...updated & applied"
cmpr.commit()


print "new files:"
for paths in cmpr.getAllNew():
    print "    cpy %s" % (paths[0], )

    if doApply:
        cmpr.newPath(paths[0])
        wrt.newPath(paths[0])
        print "    ...copied & applied"
cmpr.commit()
wrt.commit()

cmpr.destroy()
wrt.destroy()

