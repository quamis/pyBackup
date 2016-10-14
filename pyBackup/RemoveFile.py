# -*- coding: utf-8 -*-
'''
@author: lucian
'''

import argparse
import Cache.sqlite as sqlite
import SourceReader.Path as Path
import os

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--path',  dest='path',	    action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose', dest='verbose',   action='store', type=int,   default=1,help='TODO')
args = vars(parser.parse_args())

cache = sqlite.sqlite();

cache.setCacheLocation(args['cache'])
cache.initialize()

cache.log("[%s] remove path %s" % (os.path.basename(__file__), args['path']))

p = Path.Path(args['path'], False)

print cache.findFileByPath(p.path)
if cache.findFileByPath(p.path):
    cache.deleteFileFromFiles(p)
else:
    raise Exception("Cannot find specified path for deletion")

cache.commit()
cache.destroy()
