#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

# Imports future

# Imports externals
import re
import os
import sys
try:
  import psyco # 2.5 times speed improvement
  psyco.full()
except ImportError:
  pass
import subprocess

# Imports internals


class Torrent(object):
  """
  Sphinx doc.
  """

  def __init__(self, filename):
    super(Torrent, self).__init__()
    self.__filename = filename
    self.file = None # Basename in $downloadPath directory
    self.__parse()

  def __repr__(self):
    return """< Torrent "%s" contains "%s" >""" % (self.__filename, self.file)

  def __parse(self):
    fd = open(self.__filename)
    parsed = self.__bdecode(fd.read())
    fd.close()

    info = parsed.get('info')
    print info
    if info is None:
      raise RuntimeError, 'No torrent information present'
    if info.has_key('files'):
      self.file = info.get('files')[0].get('path')[0]
    else:
      self.file = info.get('name')
    if not self.file:
      raise RuntimeError, 'Not filename present'

  def __bdecode(self, data):
    chunks = list(data)
    chunks.reverse()
    root = self.__bdecodeChunk(chunks)
    return root

  def __bdecodeChunk(self, chunks):
    item = chunks.pop()
    decimalPat = re.compile('\d')
    decimal = decimalPat.findall

    if item == 'd': # Dictionary
      item = chunks.pop()
      d = dict()
      while item != 'e': # End delimiter
        chunks.append(item)
        key = self.__bdecodeChunk(chunks)
        d[key] = self.__bdecodeChunk(chunks)
        item = chunks.pop()
      return d

    elif item == 'l': # List
      item = chunks.pop()
      l = list()
      while item != 'e':
        chunks.append(item)
        l.append(self.__bdecodeChunk(chunks))
        item = chunks.pop()
      return l

    elif item == 'i': # Integer
      item = chunks.pop()
      i = ''
      while item != 'e':
        i += item
        item = chunks.pop()
      return int(i)

    elif decimal(item): # Byte string
      d = ''
      while decimal(item):
        d += item
        item = chunks.pop()
      s = ''
      for i in xrange(int(d)):
        s += chunks.pop()
      return s

    raise RuntimeError, 'Invalid data'


if __name__ == '__main__':
  import sys

  for filename in sys.argv[1:]:
    try:
      print Torrent(filename)
    except Exception, e:
      print 'Error processing "%s": %s' % (filename
          , str(e))

