# -*- coding: utf-8 -*-

'''
Created on Sep 1, 2013

@author: lucian
'''

import xml.etree.ElementTree as ET
import datetime

class worklog(object):
    '''
    Class to help reading the config file and select sections from it
    '''


    def __init__(self, xmlFile):
        '''
        setup the reader and prepare it to read the config file
        '''
        self.xmlFile = xmlFile
        self.date = datetime.datetime.now()
        
        try:
            self.loadData()
        except:
            print "init XML %s" % self.xmlFile
            self.loadDataDefault()
        
        
    def loadData(self):
        self.xml = ET.parse(self.xmlFile)
        self.xml = self.xml.getroot()
        
    def loadDataDefault(self):
        s = u"""<?xml version="1.0" encoding="UTF-8"?>
<worklog>
    <setup>
        <ctime date="%s"/>
        <mtime />
        <logs />
    </setup>
    <files />
</worklog>""" % ( self.date.isoformat('T'))
        self.xml = ET.fromstring(s)

    def append(self, f, h, s):
        e = ET.Element('file')
        if h is None:
            h = ''
        
        e.text = f.decode("utf-8")
        e.set('hash', h)
        e.set('status', s)
        self.xml.find('files').append(e)
        
    def close(self):
        self.xml.find("setup/mtime").set("time", self.date.isoformat('T'))
        
        e = ET.Element('mtime', {'date': self.date.isoformat('T')})
        self.xml.find("setup/logs").append(e)
        
        ET.ElementTree(self.xml).write(self.xmlFile, "UTF-8")