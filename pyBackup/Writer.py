# -*- coding: utf-8 -*-
'''
@author: lucian
'''
import argparse
from Comparer.CompleteComparer import CompleteComparer
from Writer.LocalPathWriter.Writer import Writer
from Writer.Backup.Writer import Writer as BackupWriter
import Cache.sqlite as sqlite
import os, sys, time, datetime
from View.ScriptStatusTracker import ScriptStatusTracker
import SourceReader.Path as Path
import logging

parser = argparse.ArgumentParser(description='Create the sqlite DB')
parser.add_argument('--cacheNew',  dest='cacheNew',	action='store', type=str,   default='',help='TODO')
parser.add_argument('--cacheOld',  dest='cacheOld', action='store', type=str,   default='',help='TODO')
parser.add_argument('--source',  dest='source', action='store', type=str,   default='',help='TODO')
parser.add_argument('--destination',  dest='destination', action='store', type=str,   default='',help='TODO')
parser.add_argument('--destinationBackup',  dest='destinationBackup', action='store', type=str,   default='',help='TODO')
parser.add_argument('--verbose',  dest='verbose', action='store', type=int,   default='',help='TODO')
parser.add_argument('--fail',  dest='fail', action='store', type=int, default=0, help='TODO')
args = vars(parser.parse_args())

class LogTracker(ScriptStatusTracker):
    def __init__(self, verbosity):
        super(LogTracker, self).__init__(verbosity)
        self.settings = {
            'resetTime':    60,
            'flushTime':    2.0,
        }
    
    def storeEvent(self, tm, event, data):
        k = "size:"+event
        if not k in self.totalEvents:
            self.totalEvents[k] = 0
            
            
        if not k in self.events:
            self.events[k] = 0
        
        if not data['path'].isDir:
            self.totalEvents[k]+= data['path'].size
            self.events[k]+= data['path'].size
        
        return super(LogTracker, self).storeEvent(tm, event, data)
        
    def composeOutputStr(self, statusStr, tm, event, data):
        mbps = "---.-Mb/s"
        if sum([self._getEvent("newFile"), self._getEvent("updateFile")])>4 and tm - self.stats['resetTime'] > 2.5:
            v = float(sum([self._getEvent("size:newFile"), self._getEvent("size:updateFile")]))/(tm - self.stats['resetTime'])/(1024*1024)
            mbps = "%5.1fMb/s" % (min(v, 999.9))
            
        return "%s%s %9s: %s" % (statusStr, mbps, event, self.pfmt.format(data['path'].path).ljust(120))
        
    def _getEvent(self, k):
        if not k in self.events:
            self.events[k] = 0
        return self.events[k]
    
    def calcStats(self, tm):
        if tm - self.stats['resetTime'] > 1.0:
            avg = (sum([self._getEvent('moveFile'), self._getEvent('newFile'), self._getEvent('deleteFile'), self._getEvent('updateFile'), ])) / (tm - self.stats['resetTime'])
            self.stats['evtps'] = avg
            self.stats['isWarmingUp'] = False


def callbackWriter(lp, event, data):
    tm = time.time()
    tracker.storeEvent(tm, event, data)
    tracker.logEvent(tm, event, data)
    

if args['verbose']>=4:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%Y%m%d %I:%M:%S')
else:
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.WARNING, datefmt='%Y%m%d %I:%M:%S')
    
    
tracker = LogTracker(args['verbose'])
#tracker = LogTracker(0)
    

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

wrtbackup = BackupWriter(args['destinationBackup'], args['destination'], args['source'], time.strftime("%Y%m%d%H%M%S"))
wrtbackup.initialize()

cacheNew.log("[%s] initialized" % (os.path.basename(__file__)))

if cacheNew.getFlag('destination.path') is None:
    cacheNew.setFlag('destination.cache.path', args['cacheOld'])
    cacheNew.setFlag('destination.path', args['destination'])
    cacheNew.setFlag('destinationBackup.path', args['destinationBackup'])
    

logging.info("moved files:")
for paths in cmpr.getMovedFiles():
    logging.info("    ren %s --> %s" % (paths[1], paths[0]))

    if doApply:
        np = Path.Path(paths[0], False)
        np.size = paths[2]
        
        op = Path.Path(paths[1], False)
        op.size = paths[3]
        
        cmpr.moveFile(op, np)
        wrt.moveFile(op, np)
        #print "    ...marked & written"
cmpr.commit()
wrt.commit()


logging.info("deleted files:")
# TODO: do some sort of backups
for paths in cmpr.getDeletedFiles():
    if args['verbose']>=4:
        logging.info("    del %s" % (paths[0]))
    
    if doApply:
        op = Path.Path(paths[0], False)
        op.size = paths[1]
        
        try:
            wrtbackup.deleteFile(op)
        except (IOError, OSError) as e:
            logging.error("cannot delete backup file: %s (%s)" % (e.strerror, op.path))
            if args['fail']<=8:
                raise e
            
        try:
            cmpr.deleteFile(op)
        except (IOError, OSError) as e:
            logging.error("cannot delete comparer file: %s (%s)" % (e.strerror, op.path))
            if args['fail']<=6:
                raise e
            
        try:
            wrt.deleteFile(op)
        except (IOError, OSError) as e:
            logging.error("cannot delete writer file: %s (%s)" % (e.strerror, op.path))
            if args['fail']<=4:
                raise e
        
        
        #print "    ...deleted & written"
cmpr.commit()
wrt.commit()


logging.info("deleted dirs:")
# TODO: do some sort of backups
for paths in cmpr.getDeletedDirs():
    if args['verbose']>=4:
        logging.info("    rmd %s" % (paths[0]))
    
    if doApply:
        op = Path.Path(paths[0], True)
        
        cmpr.deleteDir(op)
        wrt.deleteDir(op)
        #print "    ...deleted & written"
cmpr.commit()
wrt.commit()


logging.info("changed files:")
# TODO: do some sort of backups
for paths in cmpr.getChangedFiles():
    logging.info("    upd %s --> %s" % (paths[1], paths[0], ))

    if doApply:
        np = Path.Path(paths[0], False)
        np.size = paths[2]
        
        op = Path.Path(paths[1], False)
        op.size = paths[3]
        try:
            wrtbackup.updateFile(op, np)
        except (IOError, OSError) as e:
            logging.error("cannot update backup file: %s (%s, %s)" % (e.strerror, op.path, np.path))
            if args['fail']<=8:
                raise e
            
        try:
            cmpr.updateFile(op, np)
        except (IOError, OSError) as e:
            logging.error("cannot update comparer file: %s (%s, %s)" % (e.strerror, op.path, np.path))
            if args['fail']<=6:
                raise e
        
        try:
            wrt.updateFile(op, np)
        except (IOError, OSError) as e:
            logging.error("cannot update writer file: %s (%s, %s)" % (e.strerror, op.path, np.path))
            if args['fail']<=4:
                raise e
            
        
        #print "    ...updated & written"
cmpr.commit()
wrt.commit()

logging.info("new files:")
for paths in cmpr.getNewFiles():
    logging.info("    cpy %s" % (paths[0], ))

    if doApply:
        np = Path.Path(paths[0], False)
        np.size = paths[1]
        
        cmpr.newFile(np)
        wrt.newFile(np)
        #print "    ...copied & written"
cmpr.commit()
wrt.commit()


logging.info("new dirs:")
for paths in cmpr.getNewDirs():
    logging.info("    mkd %s" % (paths[0], ))

    if doApply:
        np = Path.Path(paths[0], True)
        
        cmpr.newDir(np)
        wrt.newDir(np)
        #print "    ...created & written"
cmpr.commit()
wrt.commit()


cacheNew.log("[%s] done" % (os.path.basename(__file__)))

cmpr.destroy()
wrt.destroy()

sys.stdout.write("\n")
