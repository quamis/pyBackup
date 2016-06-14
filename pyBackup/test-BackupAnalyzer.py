# -*- coding: utf-8 -*-
'''
@author: lucian
'''

import pprint
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
import Cache.sqlite as sqlite

pp = pprint.PrettyPrinter(indent=4)

cacheNew = sqlite.sqlite();
cacheNew.setCacheLocation('FileSystem.sqlite')

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

analyzer.destroy()

