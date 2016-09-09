# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import pprint
import humanize
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
import Cache.sqlite as sqlite
import os

pp = pprint.PrettyPrinter(indent=4)

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data',  dest='data', action='store', type=str,   default='',help='TODO')
args = vars(parser.parse_args())


cache = sqlite.sqlite();
cache.setCacheLocation(args['cache'])
cache.initialize()

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

#TODO: number of files per type (music/jpg/others)
#TODO: size of files per type (music/jpg/others)

print "items total:                 %s files" % (analyzer.getFilesCount())
print "items total:                 %s dirs" % (analyzer.getDirsCount())
print "size total:                  %s" % (humanize.naturalsize(analyzer.getTotalSize()))
print "    avg size:                %s" % (humanize.naturalsize(analyzer.getAvgSize()))
print "    median size:             %s" % (humanize.naturalsize(analyzer.getMedianSize()))
print "duplicated files total:      %s files" % (analyzer.getDuplicatedFilesCount())
print "duplicated files size:       %s" % (humanize.naturalsize(analyzer.getDuplicatedFilesSize()))
print "duplicated empty files :     %s files" % (analyzer.getEmptyFilesCount())
print "largest 10 files: \n         %s" % "\n         ".join((("%s (%s)" % (os.path.basename(path), humanize.naturalsize(size))) for (size, path) in analyzer.getTop10LargestFiles() if True))

print "empty dirs:                 %s" % (analyzer.getEmptyDirsCount())
print "getSizeByExtensionList(images):                 %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.jpg', '.jpeg', '.png', '.xcf'])))
print "getSizeByExtensionList(music):                 %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.mp3', ])))
print "getSizeByExtensionList(docs):                 %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.txt', '.doc', '.pdf', ])))

analyzer.destroy()


