#!/usr/bin/env python
# encoding: utf-8
'''
datcom.CLIDatCon -- shortdesc

datcom.CLIDatCon  need a description here

@author:     Isaac Jessop

@copyright:  2016 David Kovar. All rights reserved.

@license:    license

@contact:    dkovar@gmail.com
@contact:    zeek@zeeksgeeks.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
# our classes
from datfile.NotDatFile import NotDatFile
from datfile.DatFile import DatFile
from datcom.ConvertDat import ConvertDat
import traceback
from datfile.FileEnd import FileEnd

__all__ = []
__version__ = 0.1
__date__ = '2016-08-27'
__updated__ = '2016-08-27'

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
    doc_arr = __import__('__main__').__doc__.split("\n")
    program_shortdesc = doc_arr[1]
    author_name =doc_arr[5].split(':')[1]
    program_license = '''%s

  Created by %s on %s.
  Copyright 2016 David Kovar. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc,author_name, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="inputfile", help="path to the input data file filename.dat", metavar="inputfilename",nargs='+')
        parser.add_argument(dest="outputfile", help="path to the output data file filename.csv", metavar="outputfilename", nargs='+')

        # Process arguments
        args = parser.parse_args()
        #print args

        datFileName = args.inputfile[0]
        csvFileName = args.outputfile[0]
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")
            
        csvFile = open(csvFileName,'w');
        timeOffset = 0
        try:
            datFile = DatFile(datFileName)
            convertDat = ConvertDat(datFile)
            datFile.findMarkers();
            
            if datFile.motorStartTick != 0 :
                timeOffset = datFile.motorStartTick;
            if datFile.flightStartTick != -1 :
                timeOffset = datFile.flightStartTick;
            convertDat.timeOffset = timeOffset
            datFile.reset();
            convertDat.createRecords()
            convertDat.sampleRate = 30
            convertDat.csvPS = csvFile
            results = convertDat.analyze(True);
            #print results
            csvFile.close()
            print "OK"
        except (IOError , NotDatFile, FileEnd), e:
            print e

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        #profile_filename = 'datcom.CLIDatCon_profile.txt'
        profile_filename = 'CLIDatCon_profile.txt'
        print " running profile"
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        print "profile complete "
        sys.exit(0)
    sys.exit(main())
