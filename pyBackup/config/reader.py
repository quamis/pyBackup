'''
Created on Sep 1, 2013

@author: lucian
'''

import xml.etree.ElementTree as ET
import re

class reader(object):
    '''
    Class to help reading the config file and select sections from it
    '''


    def __init__(self, f):
        '''
        setup the reader and prepare it to read the config file
        '''
        self.file = f
        self.xml = ET.parse(self.file)
        
    def _unitToBytes(self, str):
        limit = None
        m = re.match("^(?P<size>[0-9\.]+)[\s]*(?P<unit>TB|GB|MB|KB|B)$", str)
        if m.group("unit")=='B':
            limit = float(m.group("size")) * (1024**0)
        if m.group("unit")=='KB':
            limit = float(m.group("size")) * (1024**1)
        elif m.group("unit")=='MB':
            limit = float(m.group("size")) * (1024**2)
        elif m.group("unit")=='GB':
            limit = float(m.group("size")) * (1024**3)
        elif m.group("unit")=='TB':
            limit = float(m.group("size")) * (1024**4)
        else:
            raise "Unknown measure unit specified in "+str
          
        return int(limit)
    
    
    def _unitToTime(self, str):
        limit = None
        m = re.match("^(?P<duration>[0-9\.]+)[\s]*(?P<unit>h|d|m|y)$", str)
        if m.group("unit")=='h':
            limit = float(m.group("duration")) * (60*60)
        elif m.group("unit")=='d':
            limit = float(m.group("duration")) * (60*60*24)
        elif m.group("unit")=='m':
            limit = float(m.group("duration")) * (60*60*24*30)
        elif m.group("unit")=='y':
            limit = float(m.group("duration")) * (60*60*24*30*12)
        else:
            raise "Unknown measure unit specified in "+str
          
        return int(limit)

        
    def general(self):
        ret = {}
        
        # http://docs.python.org/3/library/xml.etree.elementtree.html
        cfg = self.xml.find("./config")
        temp = cfg.find("./temporary")
        ret['temporary'] = []
        for item in temp.findall("./item"):
            ret['temporary'].append({ 
                'limit':    self._unitToBytes(item.attrib['limit']),
                'path':     str(item.text),
            })
            
        ret['diffStrategy'] = self._read_diffStrategy(cfg.find("./diffStrategy"))
        return ret

    
    def _read_diffStrategy(self, node):
        ret = {}
        ret['strategy'] = node.attrib['strategy']
        if ret['strategy']=='filesize':
            pass
        elif ret['strategy']=='filemtime':
            pass
        elif ret['strategy']=='filesize_filemtime':
            pass
        elif ret['strategy']=='hash':
            ret['hash'] = node.find("./hash/hash").text
            
        return ret
    
    def _read_input(self, node):
        ret = {}
        ret['path'] = node.find("./path").text
        ret['recurse'] = True if node.find("./path").attrib['recurse'] in ('True', 'true', '1', 'yes') else False
        
        return ret
        
    
    def _read_output(self, node):
        ret = {}
        ret['path'] = str(node.find("./path").text)
        
        strategy = {}
        strategy['strategy'] = node.find("./strategy").attrib['strategy']
        if strategy['strategy']=='copy':
            pass
        elif strategy['strategy']=='auto':
            strategy['compress_after'] = self._unitToTime(node.find("./strategy/auto/compress/after").text)
            strategy['compress_type'] = node.find("./strategy/auto/compress/type").text
            strategy['compress_strength'] = node.find("./strategy/auto/compress/strength").text
        elif strategy['strategy']=='archiveDir':
            strategy['compress_type'] = node.find("./strategy/archiveDir/type").text
            strategy['compress_strength'] = node.find("./strategy/archiveDir/strength").text
        elif strategy['strategy']=='archiveFile':
            strategy['compress_type'] = node.find("./strategy/archiveFile/type").text
            strategy['compress_strength'] = node.find("./strategy/archiveFile/strength").text
        
        ret['strategy'] = strategy
            
        return ret

    
    def locations(self):
        ret = []
        locations = self.xml.findall("./locations/location")
        for locxml in locations:
            loc = {}
            loc['input'] = self._read_input(locxml.find("./input"))
            loc['output'] = self._read_output(locxml.find("./output"))
            loc['diffStrategy'] = self._read_diffStrategy(locxml.find("./diffStrategy"))
            
            loc['input']
            
            ret.append(loc)
        
        return ret
    
    
    
    