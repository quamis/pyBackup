# -*- coding: utf-8 -*-
'''
@author: lucian
'''

import argparse
import Cache.sqlite as sqlite
import os

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose', dest='verbose',   action='store', type=int,   default=1,help='TODO')
parser.add_argument('--optimize', dest='optimize',   action='store', type=int,   default=1, help='TODO')
parser.add_argument('--removeOldLeafs', dest='removeOldLeafs',   action='store', type=int,   default=1, help='TODO')
args = vars(parser.parse_args())

cache = sqlite.sqlite();

cache.setCacheLocation(args['cache'])
cache.initialize()

cache.log("[%s] initialize" % (os.path.basename(__file__)))

if args['removeOldLeafs']:
    cache.log("[%s] removeOldLeafs" % (os.path.basename(__file__)))
    if args['verbose']>4:
        print "removeOldLeafs"
    cache.removeOldLeafs()
    
if args['optimize']:
    cache.log("[%s] optimize" % (os.path.basename(__file__)))
    if args['verbose']>4:
        print "optimize"
    cache.optimize()

cache.log("[%s] done" % (os.path.basename(__file__)))
cache.commit()
cache.destroy()
