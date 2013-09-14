# -*- coding: utf-8 -*-

'''
Created on Sep 1, 2013

@author: lucian
'''

import xml.etree.ElementTree as ET
import datetime
import gzip

import worklog

class cache(worklog.worklog):
    '''
    Class to help reading the cache file and select sections from it
    '''
    def __init__(self, xmlFile):
        worklog.worklog.__init__(self, xmlFile)
        self.existingData = {}
        self.newData = {}
        
    def loadData(self):
        f = gzip.open(self.xmlFile+".gz", 'rb')
        self.xml = ET.fromstring(f.read())
        f.close()
        
    def loadDataDefault(self):
        worklog.worklog.loadDataDefault(self)
        print "Initialize cache file %s.gz" % self.xmlFile
    
    def open(self):
        for tag in self.xml.findall("files/file"):
            self.existingData[tag.text] = tag.attrib
            
    def exists(self, p):
        return p in self.existingData
    
    def getHash(self, p):
        return self.get(p)['hash']
    
    def get(self, p):
        item = self.existingData[p]
        ret = {
           'file': p,
           'hash': item['h'],
           'status': item['s'],
           'size': int(item['sz']),
           'mtime': float(item['mt']),
        }
        return ret
    
    def set(self, p, item):
        self.newData[p] = item
        
    def close(self):
        files = self.xml.find('files')
        files.clear()
        for p in self.newData:
            item = self.newData[p] 
            e = ET.Element('file')

            e.text = (p if p else '').decode("utf-8")
            e.set('h', item['hash'] if item['hash'] else '')
            e.set('s', item['status'] if item['status'] else '')
            e.set('sz', str(item['size']) if item['size'] else '0')
            e.set('mt', str(float(item['mtime'])) if item['mtime'] else '0.0')
            files.append(e)
        
        self.xml.find("setup/mtime").set("time", self.date.isoformat('T'))
        e = ET.Element('mtime', {'date': self.date.isoformat('T')})
        
        f = gzip.open(self.xmlFile+".gz", 'wb')
        f.write(ET.tostring(self.xml, "UTF-8"))
        f.close()
