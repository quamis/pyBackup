from View.PathFormatter import PathFormatter
import sys, time

class ScriptStatusTracker(object):
    def __init__(self, verbosity):
        self.verbosity = verbosity
        self.pfmt = PathFormatter(120)
        t = time.time()
        self.stats = {
            'startTime':    t,
            'resetTime':    t,
            'flushTime':    t,
            'statsTime':    t,
            'evtps':        0.0, 
            'evtpg':        0.0, 
            'totalEvents':  0,
            'expectedEvents':None,
            'isWarmingUp': True, 
        }
        
        self.events = {}
        self.totalEvents = {}
        
        
        self.settings = {
            'resetTime':    30,
            'flushTime':    1,
        }

    
    def storeEvent(self, tm, event, data):
        if self.verbosity==0:
            return
            
        if not event in self.events:
            self.events[event] = 0
        self.events[event]+= 1
        
        if not event in self.totalEvents:
            self.totalEvents[event] = 0
        self.totalEvents[event]+= 1
        
        self.stats['totalEvents']+= 1
        
    def resetStats(self, tm):
        
        self.stats['resetTime'] =    tm
        #stats['evtps'] =        0
        self.stats['isWarmingUp'] =  True
        
        self.events =           {}
            
        
    def calcStats(self, tm):
        pass

            
    def composeOutputStr(self, statusStr, event, data):
        return "%s %8s: %s" % (statusStr, event, self.pfmt.format(data['p'].path).ljust(120))
        
    def logEvent(self, tm, event, data):
        if self.verbosity==0:
            return
    
        doHandle = False
        if self.verbosity>=3:
            doHandle = True
        elif self.verbosity>=2:
            doHandle = True    
        elif self.verbosity>=1:
            if tm - self.stats['statsTime'] > 0.1:
                doHandle = True
            
        if doHandle:
            self.stats['statsTime'] = tm
            evtps = " ....e/s,"
            if not self.stats['isWarmingUp']:
                evtps = "%5.1fe/s," % (min(self.stats['evtps'], 9999.9))
                
            pgpc = "--.-%,"
            if not self.stats['expectedEvents'] is None:
                pgpc = "%4.1f%%," % (99.9*self.stats['evtpg'])
                
            
            self.calcStats(tm)
            
            self.printEvent(tm, self.composeOutputStr("%s%s" % (pgpc, evtps), tm, event, data))
        
            if tm - self.stats['resetTime'] > self.settings['resetTime']:
                self.resetStats(tm)
        
    def printEvent(self, tm, str):
        if self.verbosity>=3:
            sys.stdout.write("\n%s" % (str))
            sys.stdout.flush()
        else:
            sys.stdout.write("\r%s" % (str))
            if tm - self.stats['flushTime'] > self.settings['flushTime']:
                self.stats['flushTime'] = tm
                sys.stdout.flush()
    
    def printStr(self, str):
        sys.stdout.write("\n%s" % (str))
        