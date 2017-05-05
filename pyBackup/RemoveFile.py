# -*- coding: utf-8 -*-
'''
@author: lucian
'''

import argparse
import Cache.sqlite as sqlite
from Writer.LocalPathWriter.Writer import Writer
from Writer.Backup.Writer import Writer as BackupWriter
import SourceReader.Path as Path
import os, glob, time

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--doApply',                dest='doApply',     action='store', type=int,   default=0, help='TODO')
parser.add_argument('--cache',                  dest='cache',	action='store',   type=str,   default='',help='TODO')
parser.add_argument('--destination',            dest='destination',         action='store', type=str,   default='auto',help='TODO')
parser.add_argument('--destinationBackup',      dest='destinationBackup',         action='store', type=str,   default='auto',help='TODO')
parser.add_argument('--source',                 dest='source',         action='store', type=str,   default='auto',help='TODO')
parser.add_argument('--onlyFromCache',          dest='onlyFromCache',     action='store', type=int,   default=0, help='TODO')
parser.add_argument('--path',                   dest='path',	    action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose',                dest='verbose',   action='store', type=int,   default=1,help='TODO')
args = vars(parser.parse_args())

cache = sqlite.sqlite();

cache.setCacheLocation(args['cache'])
cache.initialize()

if args['destination']=='auto':
    args['destination'] = cache.getFlag('destination.path')
    print "autoload destination: %s" % (args['destination'])

if args['source']=='auto':
    args['source'] = cache.getFlag('source.path')
    print "autoload source:      %s" % (args['source'])
    

wrt = Writer(args['destination'], args['source'])
wrt.initialize()

wrtbackup = BackupWriter(args['destinationBackup'], args['destination'], args['source'], time.strftime("%Y%m%d%H%M%S"))
wrtbackup.initialize()

#glob.glob('./[0-9].*')
paths = cache.findFilesByPath(args['path'].replace("*", "%"))

print "trying to delete %d paths from %s" % (len(paths), args['path'])

for (path, ) in paths:
    print ("    remove %s" % (path))
    if args['doApply']:
        cache.log("[%s] remove path %s, onlyFromCache: %d" % (os.path.basename(__file__), path, args['onlyFromCache']))
        p = Path.Path(path, False)
        
        if cache.findFileByPath(p.path):
            cache.deleteFileFromFiles(p)
            if not args['onlyFromCache']:
                try:
                    wrtbackup.deleteFile(p)
                    print ("    backed-up")
                except (OSError, IOError):
                    print ("    os error on backup")
                
                
                try:
                    wrt.deleteFile(p)
                    print ("    hard removed")
                except (OSError, IOError):
                    print ("    os error")
        else:
            raise Exception("Cannot find specified path for deletion")

cache.commit()
cache.destroy()
