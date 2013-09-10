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
            self.xml = ET.parse(self.xmlFile)
            self.xml = self.xml.getroot()
        except:
            s = """<?xml version="1.0" encoding="UTF-8"?>
<worklog>
    <setup>
        <ctime date="%s"/>
        <mtime />
        <logs />
    </setup>
    <files />
</worklog>""" % ( self.date.isoformat('T'))
            self.xml = ET.fromstring(s)
        

    def append(self, f, h):
        e = ET.Element('file')
        e.text = f
        e.set('hash', h)
        self.xml.find('files').append(e)
        
    def close(self):
        self.xml.find("setup/mtime").set("time", self.date.isoformat('T'))
        
        e = ET.Element('mtime', {'date': self.date.isoformat('T')})
        self.xml.find("setup/logs").append(e)
        
        ET.ElementTree(self.xml).write(self.xmlFile, "UTF-8")