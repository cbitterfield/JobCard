#!/usr/bin/python
# encoding: utf-8
'''
getvideoinfo -- shortdesc

getvideoinfo is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2017 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import job
import yaml

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2017-12-08'
__updated__ = '2017-12-08'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

#===============================================================================
# Setup  Logging
#===============================================================================
import logging
import logging.config



logger = logging.getLogger(__name__)

logging.basicConfig(disable_existing_loggers=False,format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


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
  Copyright 2017 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-l","--logfile", action="store", help="Write Logfile if ommitted write to STDOUT")
        parser.add_argument('-p', '--path', action='store', default='.', help="Use this path for processing")
        parser.add_argument("-c","--configfile", default="config.yml", help="use config file, default is config.yml in working dir")

        # Process arguments
        args = parser.parse_args()
        print args

        path = args.path
        verbose = args.verbose
        recurse = args.recurse
        inpat = args.include
        expat = args.exclude
        logfile = args.logfile
        
        # Error Check all directories
        
        if os.path.isdir(path):
            logger.info("Directory exists: " + str(path))
        
        
        # Load Config file
        # Open Config File

        if os.path.isfile(args.configfile):
            logger.info("Config file exists")
            cfg = open(args.configfile,'r')
            config = yaml.load(cfg)
            
        else:
            logger.info("Missing Config File")
            return 3
    
        

        if verbose > 0:
            print("Verbose mode on")
            if recurse:
                print("Recursive mode on")
            else:
                print("Recursive mode off")

        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")

        if not logfile:            
            base = os.path.basename(logfile)
            logfile = os.path.splitext(base)[0] + ".log"
        else:
            logfile = args.logfile

        logger.info("Logfile: " + str(logfile))   
        log = open(logfile,'w')
        log.write("filePath,filename,md5,width,height,bitrate,duration\n")
        
        # Code execution goes here
        logger.info("Review Directory " + str(path))
        for root, dirs, files in os.walk(path,followlinks=True):
            for folder in dirs:
                for file in files:
                    filePath = os.path.join(root,file)
                    if file.endswith(inpat):                           
                        logger.info(file)
                        MD5 = job.getmd5(config,filePath,False)
                        md5 = MD5.rstrip()
                        Error, height, width, myduration, mybitrate = job.videosize(filePath, config, False)
                        log.write(filePath + ","+ file + ","+ md5 + "," + width + "," + height + "," + mybitrate + "," + myduration + "\n")
                    
                    
        log.close()       
        return 0
    
    
    
    
    
    
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        log.close()
        return 1
    except Exception, e:
        logger.error("ERROR Exception: " + str(e))
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 4

if __name__ == "__main__":
    print "start processing"


    sys.exit(main())