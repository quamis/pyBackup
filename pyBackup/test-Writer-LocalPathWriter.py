# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import pprint
from Comparer.CompleteComparer import CompleteComparer
from Writer.LocalPathWriter.Writer import Writer
import Cache.sqlite as sqlite
import os
import sys

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cacheNew',  dest='cacheNew',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--cacheOld',  dest='cacheOld', action='store', type=str,   default='',help='TODO')
parser.add_argument('--source',  dest='source', action='store', type=str,   default='',help='TODO')
parser.add_argument('--destination',  dest='destination', action='store', type=str,   default='',help='TODO')
args = vars(parser.parse_args())

def formatPath(p, l):
    o = ""
    if len(p)>l:
        o = "%s...%s" % (p[0:50], p[-(l-50-3):])
    else:
        o = "%s" % (p)
    return o

def callbackWriter(lp, event, data):
    if event=='moveFile':
        if not data['isDir']:
            sys.stdout.write("\r rename: %50s" % (formatPath(data['path'], 120).ljust(120)))
            
    if event=='newFile':
        if not data['isDir']:
            sys.stdout.write("\r new   : %50s" % (formatPath(data['path'], 120).ljust(120)))
            
    if event=='deleteFile':
        if not data['isDir']:
            sys.stdout.write("\r delete: %50s" % (formatPath(data['path'], 120).ljust(120)))
            
    if event=='updateFile':
        if not data['isDir']:
            sys.stdout.write("\r update: %50s" % (formatPath(data['path'], 120).ljust(120)))


cacheNew = sqlite.sqlite();
cacheNew.setCacheLocation(args['cacheNew'])
cacheNew.initialize()

cacheNew.log("[%s] start" % (os.path.basename(__file__)))

cacheOld = sqlite.sqlite();
cacheOld.setCacheLocation(args['cacheOld'])
cacheOld.initialize()

doApply = True
cmpr = CompleteComparer()

cmpr.setNewCache(cacheNew)
cmpr.setOldCache(cacheOld)
cmpr.initialize()

wrt = Writer(args['destination'], args['source'])
wrt.initialize()

wrt.registerProgressCallback(callbackWriter)

cacheNew.log("[%s] initialized" % (os.path.basename(__file__)))


#print "moved files:"
for paths in cmpr.getMovedFiles():
    #print "    ren %s --> %s" % (paths[1], paths[0])

    if doApply:
        cmpr.moveFile(paths[1], paths[0])
        wrt.moveFile(paths[1], paths[0])
        #print "    ...marked & written"
cmpr.commit()
wrt.commit()


#print "deleted files:"
# TODO: do some sort of backups
for paths in cmpr.getDeletedFiles():
    #print "    del %s" % (paths[0])
    
    if doApply:
        cmpr.deleteFile(paths[0])
        wrt.deleteFile(paths[0])
        #print "    ...deleted & written"
cmpr.commit()
wrt.commit()

#print "deleted dirs:"
# TODO: do some sort of backups
for paths in cmpr.getDeletedDirs():
    #print "    rmd %s" % (paths[0])
    
    if doApply:
        cmpr.deleteDir(paths[0])
        wrt.deleteDir(paths[0])
        #print "    ...deleted & written"
cmpr.commit()
wrt.commit()


#print "changed files:"
# TODO: do some sort of backups
for paths in cmpr.getChangedFiles():
    #print "    upd %s --> %s" % (paths[1], paths[0], )

    if doApply:
        cmpr.updateFile(paths[1], paths[0])
        wrt.updateFile(paths[1], paths[0])
        #print "    ...updated & written"
cmpr.commit()
wrt.commit()


#print "new files:"
for paths in cmpr.getNewFiles():
    #print "    cpy %s" % (paths[0], )

    if doApply:
        cmpr.newFile(paths[0])
        wrt.newFile(paths[0])
        #print "    ...copied & written"
cmpr.commit()
wrt.commit()


#print "new dirs:"
for paths in cmpr.getNewDirs():
    #print "    mkd %s" % (paths[0], )

    if doApply:
        cmpr.newDir(paths[0])
        wrt.newDir(paths[0])
        #print "    ...created & written"
cmpr.commit()
wrt.commit()


cacheNew.log("[%s] done" % (os.path.basename(__file__)))

cmpr.destroy()
wrt.destroy()

