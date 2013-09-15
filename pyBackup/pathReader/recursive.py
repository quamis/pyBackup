'''
Created on Sep 7, 2013

@author: lucian
'''
import os, sys, fnmatch, re;

class recursive(object):
    '''
    Recurse through a folder and return file-by-file
    '''


    def __init__(self, path, options):
        '''
        Initialize the parser
        '''
        self.path = path
        self.options = options
        
    def base(self):
        return self.path

    def _matchesFilers(self, type, path):
        if 'ignore' not in self.options:
            return False
        
        for opt in self.options['ignore']:
            apply = False
            if opt['target'] == 'all' or opt['target'] == type:
                apply = True
            if apply:
                regex = None
                if opt['type']=='regex':
                    regex = opt['content']
                if opt['type']=='startswith':
                    regex = "^"+re.escape(opt['content'])
                if opt['type']=='endswith':
                    regex = re.escape(opt['content'])+"$"
                if opt['type']=='contains':
                    regex = re.escape(opt['content'])
                if opt['type']=='is':
                    regex = "^"+re.escape(opt['content'])+"$"
                    
                if re.search(regex, path, re.IGNORECASE):
                    return True
            
        return False
        
    def getAll(self):
        paths = []
        for root, dirs, files in os.walk(self.path):
            for basename in files:
                filename = os.path.join(root, basename)[len(self.path):]
                if not self._matchesFilers('file', filename):
                    paths.append(filename)
                    
            for basename in dirs:
                filename = os.path.join(root, basename)[len(self.path):] + "/"
                if not self._matchesFilers('dir', filename):
                    paths.append(filename)
                    
        return paths
