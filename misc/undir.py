#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

# subversion info:
# $HeadURL: https://skasi-lps.googlecode.com/svn/trunk/templates/exec_tpl.py $
# $Author: SkAsI.7 $
# $Id: exec_tpl.py 34 2011-02-04 10:52:00Z SkAsI.7 $
# $Revision: 34 $


# Pychecker options
__pychecker__ = 'no-callinit no-classattr'

# External imports
import logging
import optparse
import os
import sys

# Internal imports (if any)

def undir(root, rem_levels):
  if rem_levels == 0:
    for root_, dirs, files in os.walk(root, topdown=False):
      if root_ != root: # Avoid renaming same files
        for file_ in files:
          logging.info('Moving %s to %s' % (os.path.join(root_, file_), os.path.join(root, file_)))
          os.rename(os.path.join(root_, file_), os.path.join(root, file_))
      for dir_ in dirs:
        logging.info('Removing %s' % (os.path.join(root_, dir_)))
        os.rmdir(os.path.join(root_, dir_))
  else:
    logging.info('Entering into %s (remaining levels: %d)' % (root, rem_levels))
    entries = [os.path.join(root, entry) for entry in os.listdir(root)]
    entries = [entry for entry in entries if os.path.isdir(entry)]
    for entry in entries:
      undir(os.path.join(root, entry), rem_levels - 1)


# Main entry point
if __name__ == '__main__':
  parser = optparse.OptionParser(usage="uso: %prog [options] <root_dir>")
  parser.add_option('-l', '--log_level', dest='logLevel', default='INFO',
      help='log level [INFO]')
  programName, _ = os.path.splitext(sys.argv[0])
  parser.add_option('-f', '--log_file', dest='logFile', default='%s.log' % programName,
      help='log file [%s.log]' % programName)
  parser.add_option('-u', '--user', dest='user', default='my_user',
      help='print user [my_user]')
  parser.add_option('-d', '--depth', dest='depth', default=0,
      type='int', help='directories\' allowed depth')
  (options, args) = parser.parse_args()

  loggingFormat = '%(asctime)s %(levelname)s %(message)s'
  numericLevel = getattr(logging, options.logLevel.upper(), None)
  if not isinstance(numericLevel, int):
    print 'ERROR: Invalid log level: %s' % options.logLevel
    sys.exit(2)
  if options.logFile == '-':
    options.logFile = None

  # Define logging
  logging.basicConfig(format=loggingFormat, level=numericLevel, filename=options.logFile, filemode='w')

  if len(args) != 1:
    parser.print_usage()
    sys.exit(1)
  root_dir, = args

  undir(root_dir, options.depth)

