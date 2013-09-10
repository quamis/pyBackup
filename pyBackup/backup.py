#!/usr/bin/python
# encoding: utf-8
'''
backup -- process the config file & perform the backup

backup is a script to help me backing up my important stuff fron my local desktop to my external hdd

It defines classes_and_methods

@author:     quamis@gmail.com
        
@copyright:  2013 quamis@gmail.com. All rights reserved.
        
@license:    license

@contact:    quamis@gmail.com
@deffield    updated: 2013-09-01
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import config.reader
import config.worklog

import pathReader.recursive
import pathReader.linear

import pathWriter.copy

import fileComparer.filesize
import fileComparer.filemtime
import fileComparer.hash

import folderComparer.general

import worker.general
from config.worklog import worklog




__all__ = []
__version__ = 0.1
__date__ = '2013-09-01'
__updated__ = '2013-09-01'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-c", "--config", dest="config", action="store", type=file, default=None, help="the xml config file")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        
        """
        if verbose > 0:
            print("Verbose mode on")
            if recurse:
                print("Recursive mode on")
            else:
                print("Recursive mode off")
        """
        
        if args.config is None:
            raise CLIError("No config specified, nothing will be processed")
        
        cfgReader = config.reader.reader("config.xml")
        #print reader.general()
        #print reader.locations()
        for loc in cfgReader.locations():
            print "backup %s, %s" % (loc['input']['path'], "recursive" if loc['input']['recurse'] else "non-recursive")
            print "    save to %s, %s" % (loc['output']['path'], loc['output']['strategy']['strategy'])
            
            reader1 = None
            reader2 = None
            if loc['input']['recurse']==True:
                reader1 = pathReader.recursive.recursive(loc['input']['path'], loc['input'])
                reader2 = pathReader.recursive.recursive(loc['output']['path'], loc['input'])
            if loc['input']['recurse']==False:
                reader1 = pathReader.linear.linear(loc['input']['path'], loc['input'])
                reader2 = pathReader.linear.linear(loc['output']['path'], loc['input'])
                
            writer = None
            if loc['output']['strategy']['strategy']=='copy':
                writer = pathWriter.copy.copy(loc['output']['path'], loc['output']['strategy'])
            
            fComparer = None
            if loc['diffStrategy']['strategy']=='filesize':
                fComparer = fileComparer.filesize.filesize(loc['diffStrategy'])
            if loc['diffStrategy']['strategy']=='filemtime':
                fComparer = fileComparer.filemtime.filemtime(loc['diffStrategy'])
            if loc['diffStrategy']['strategy']=='hash':
                fComparer = fileComparer.hash.hash(loc['diffStrategy'])

            dComparer = folderComparer.general.general(fComparer, {})
            
            # run the actual worker
            wrk = worker.general.general(reader1, reader2, writer, fComparer)
            wrk.run()
            
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + " " + str(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        sys.stderr.write("\n")
        return 2

if __name__ == "__main__":
    if DEBUG:
        pass
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'backup_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    sys.exit(main())