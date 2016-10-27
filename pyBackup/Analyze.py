# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
import humanize
from BackupAnalyzer.BackupAnalyzer import BackupAnalyzer
import Cache.sqlite as sqlite
import os, datetime


parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cache',  dest='cache',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--data',  dest='data', action='store', type=str,   default='',help='TODO')
parser.add_argument('--mode',  dest='mode', action='store', type=str,   default='auto',help='TODO')
args = vars(parser.parse_args())


cache = sqlite.sqlite();
cache.setCacheLocation(args['cache'])
cache.initialize()

analyzer = BackupAnalyzer()
analyzer.setCache(cache)
analyzer.initialize()

if args['mode']=='auto':
    print "items total:                 %d files" % (analyzer.getFilesCount())
    print "items total:                 %d dirs" % (analyzer.getDirsCount())
    print "size total:                  %s" % (humanize.naturalsize(analyzer.getTotalSize()))
    print "    avg size:                %s" % (humanize.naturalsize(analyzer.getAvgSize()))
    print "    median size:             %s" % (humanize.naturalsize(analyzer.getMedianSize()))
    print "duplicated files total:      %s files" % (analyzer.getDuplicatedFilesCount())
    print "duplicated files size:       %s" % (humanize.naturalsize(analyzer.getDuplicatedFilesSize()))
    print "duplicated empty files :     %s files" % (analyzer.getEmptyFilesCount())
    print "largest 10 files: \n         %s" % "\n         ".join((("%s (%s)" % (os.path.basename(path), humanize.naturalsize(size))) for (size, path) in analyzer.getTop10LargestFiles() if True))

    print "empty dirs:                 %s" % (analyzer.getEmptyDirsCount())
    print "getSizeByExtensionList(images): %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.jpg', '.jpeg', '.png', '.xcf'])))
    print "getSizeByExtensionList(music):  %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.mp3', ])))
    print "getSizeByExtensionList(video):  %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.avi', '.mpg', '.mpeg', '.3gp', '.mp4', '.wma', ])))
    print "getSizeByExtensionList(iso):    %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.iso', '.cue', '.bin', ])))
    print "getSizeByExtensionList(docs):   %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.txt', '.doc', '.rtf', ])))
    print "getSizeByExtensionList(pdfs):   %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.pdf', '.ps', ])))
    print "getSizeByExtensionList(ebook):  %s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.epub', '.mobi', '.cbz', '.cbr', ])))
    print "getSizeByExtensionList(archive):%s" % (humanize.naturalsize(analyzer.getSizeByExtensionList(['.gz', '.tgz', '.tar', '.rar', '.zip', '.7z', '.bz2', ])))

    print "getFilesWithFullHashesCount:    %d files (%.2f%%)" % (analyzer.getFilesWithFullHashesCount(), 100*(float(analyzer.getFilesWithFullHashesCount())/analyzer.getFilesCount()))
elif args['mode']=='flags':
    print "first run: %s" % ( datetime.datetime.fromtimestamp(int(cache.getFlag('app.run.first'))).strftime('%Y-%m-%d %H:%M:%S'))
    print "last run:  %s" % ( datetime.datetime.fromtimestamp(int(cache.getFlag('app.run.last'))).strftime('%Y-%m-%d %H:%M:%S'))
    print "run count: %s" % ( cache.getFlag('app.run.count'))

analyzer.destroy()
cache.destroy()


