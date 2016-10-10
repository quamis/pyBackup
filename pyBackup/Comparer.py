# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import logging
import humanize
from Comparer.SimpleComparer import SimpleComparer
from Comparer.CompleteComparer import CompleteComparer
import Cache.sqlite as sqlite


parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cacheNew',  dest='cacheNew',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--cacheOld',  dest='cacheOld', action='store', type=str,   default='',help='TODO')
parser.add_argument('--source',  dest='source', action='store', type=str,   default='',help='TODO')
parser.add_argument('--destination',  dest='destination', action='store', type=str,   default='',help='TODO')
parser.add_argument('--destinationBackup',  dest='destinationBackup', action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose',  dest='verbose', action='store', type=int,   default='',help='TODO')
args = vars(parser.parse_args())

if args['verbose']>=4:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%Y%m%d %I:%M:%S')
else:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.WARNING, datefmt='%Y%m%d %I:%M:%S')
    

cacheNew = sqlite.sqlite();
cacheNew.setCacheLocation(args['cacheNew'])
cacheNew.initialize()

cacheOld = sqlite.sqlite();
cacheOld.setCacheLocation(args['cacheOld'])
cacheOld.initialize()

cmpr = CompleteComparer()

cmpr.setNewCache(cacheNew)
cmpr.setOldCache(cacheOld)
cmpr.initialize()


stats = {
    'count': {
        'getMovedFiles' :   0,
        'getDeletedFiles' : 0,
        'getChangedFiles' : 0,
        'getNewFiles' :     0,
    },
    
    'sizes': {
        'getMovedFiles' :   0,
        'getDeletedFiles' : 0,
        'getChangedFiles' : 0,
        'getNewFiles' :     0,
    },
}


for paths in cmpr.getMovedFiles():
    logging.debug("    ren %s --> %s" % (paths[1], paths[0]))
    stats['sizes']['getMovedFiles']+= paths[2]
    stats['count']['getMovedFiles']+= 1


for paths in cmpr.getDeletedFiles():
    logging.debug("    del %s" % (paths[0]))
    stats['sizes']['getDeletedFiles']+= paths[1]
    stats['count']['getDeletedFiles']+= 1


for paths in cmpr.getChangedFiles():
    logging.debug("    upd %s --> %s" % (paths[1], paths[0], ))
    stats['sizes']['getChangedFiles']+= paths[2]
    stats['count']['getChangedFiles']+= 1


for paths in cmpr.getNewFiles():
    logging.debug("    cpy %s" % (paths[0], ))
    stats['sizes']['getNewFiles']+= paths[1]
    stats['count']['getNewFiles']+= 1


print("getChangedFiles : %d files, %s" % (stats['count']['getChangedFiles'], humanize.naturalsize(stats['sizes']['getChangedFiles'])))
print("getNewFiles :     %d files, %s" % (stats['count']['getNewFiles'], humanize.naturalsize(stats['sizes']['getNewFiles'])))
print("getMovedFiles :   %d files, %s" % (stats['count']['getMovedFiles'], humanize.naturalsize(stats['sizes']['getMovedFiles'])))
print("getDeletedFiles : %d files, %s" % (stats['count']['getDeletedFiles'], humanize.naturalsize(stats['sizes']['getDeletedFiles'])))

avgTransferSpeed = 17.5 #  20.0 Mb/s can be written on the target drive
avgTransferFiles = 2000 #  2000 files/s can be altered on the target drive
print("ETA : %.2f minutes to transfer" % ( \
    ( \
        0
        + float(stats['sizes']['getChangedFiles']+stats['sizes']['getNewFiles'])/(avgTransferSpeed*1024*1024)    # Mb/s \
        + float(stats['count']['getChangedFiles']+stats['count']['getNewFiles']+stats['count']['getMovedFiles']+stats['count']['getDeletedFiles'])/(avgTransferFiles)    # files/s \
    ) \
    /(1*60)))
    
cmpr.destroy()
cacheNew.destroy()
cacheOld.destroy()
