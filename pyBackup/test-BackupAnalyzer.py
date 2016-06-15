# -*- coding: utf-8 -*-
'''
@author: lucian
'''

import pprint
import humanize
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
import Cache.sqlite as sqlite
import os

pp = pprint.PrettyPrinter(indent=4)

cache = sqlite.sqlite();
cache.setCacheLocation('FileSystem.sqlite')

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

print "items total:                 %s files" % (analyzer.getTotalCount())
print "size total:                  %s" % (humanize.naturalsize(analyzer.getTotalSize()))
print "    avg size:                %s" % (humanize.naturalsize(analyzer.getAvgSize()))
print "    median size:             %s" % (humanize.naturalsize(analyzer.getMedianSize()))
print "duplicated files total:      %s files" % (analyzer.getDuplicatedFilesCount())
print "duplicated files size:       %s" % (humanize.naturalsize(analyzer.getDuplicatedFilesSize()))
print "duplicated empty files :     %s files" % (analyzer.getEmptyFilesCount())
print "largest 10 files: \n         %s" % "\n         ".join((("%s (%s)" % (os.path.basename(path), humanize.naturalsize(size))) for (size, path) in analyzer.getTop10LargestFiles() if True))

analyzer.destroy()


