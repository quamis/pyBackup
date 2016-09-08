# -*- coding: utf-8 -*-
'''
@author: lucian
'''

"""
run as 
    rm ./FileSystem.sqlite; python ./test-Hasher-FastContentHashV1Cached.py
"""
import argparse
import pprint
from SourceReader.LocalPathReader import LocalPathReaderCached
from SourceReader.LocalPathReader import LocalPathReader
from Hasher.FastContentHashV1 import FastContentHashV1
from Hasher.FastContentHashV1 import FastContentHashV1Cached
import Cache.sqlite as sqlite

import sys

def callbackLocalPathReader(lp, event, data):
    if event=='newPath':
        if data['isDir']:
            p = data['p'].path
            o = ""
            if len(p)>120:
                o = "%s...%s" % (p[0:50], p[-67:])
            else:
                o = "%s" % (p)
            sys.stdout.write("\r scan fs: %50s" % (o.ljust(120)))
            
    if event=='getNext':
        if data['p'].isDir:
            p = data['p'].path
            o = ""
            if len(p)>120:
                o = "%s...%s" % (p[0:50], p[-67:])
            else:
                o = "%s" % (p)
            sys.stdout.write("\r cache %50s" % (o.ljust(120)))
pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data', 	dest='data',   action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose', dest='verbose',   action='store', type=int,   default=1,help='TODO')
args = vars(parser.parse_args())



cache = sqlite.sqlite();

lp = LocalPathReaderCached.LocalPathReaderCached()
lp.setCache(cache)
#lp = LocalPathReader.LocalPathReader()

cache.setCacheLocation(args['cache'])
lp.setPath(args['data'])

lp.registerProgressCallback(callbackLocalPathReader)
lp.initialize()

hh = FastContentHashV1Cached.FastContentHashV1Cached()
hh.setCache(cache)
hh.initialize()

if args['verbose']>0:
    print "-"*80
    for p in iter(lambda:lp.getNext(), None):
        print p.path
        if not p.isDir:
            print "    "+hh.hash(p)
    print "-"*80
else:
    for p in iter(lambda:lp.getNext(), None):
        if not p.isDir:
            hh.hash(p)
    
    
lp.destroy()
hh.destroy()
