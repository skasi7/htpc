#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

__pychecker__ = 'no-callinit no-classattr'


import BeautifulSoup
import mechanize
import os
import os.path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import urllib


class Browser(object):

  def __init__(self):
    object.__init__(self)
    self.__torrents_url = 'http://www.newpct.com/buscar-descargas/'
    self.__browser = mechanize.Browser()
    self.__browser.set_handle_robots(False)

  def __search(self, searchTxt):
    try: # Logging in
      print self.__browser.forms()
      self.__browser.select_form(name='searchforms')
      self.__browser.form['q'] = searchTxt
      self.__browser.submit()
    except mechanize.FormNotFoundError, e:
      pass # Already logged in

  def __download_link(self, url, output_dir, filename):
    self.__browser.open(url)
    # print self.__browser.response().read()

    try:
      link = self.__browser.find_link(url_regex=r'descargar\/index.php')
    except mechanize.LinkNotFoundError, e:
      print 'Error (link not found error): %s' % str(e)
      return False

    # print link.url
    self.__browser.follow_link(link)
    fd = tempfile.NamedTemporaryFile(delete=False)
    fd.write(self.__browser.response().read())
    fd.close()

    ret_value = subprocess.call(['deluge-console', 'add', fd.name]
            , stdout=open('/dev/null', 'w+b'), stderr=subprocess.STDOUT)
    if ret_value == 0:
      # Delete temp file
      os.unlink(fd.name)
      print '[*] Added to deluge:', filename
    else:
      # Move temp file
      filename = os.path.join(output_dir, filename)
      shutil.move(fd.name, filename)
      print '[*] Wrote:', filename

  def enumerate_links(self, output_dir='.', searchTxt=None):
    download_all = False

    self.__browser.open(self.__torrents_url, data=urllib.urlencode(dict(q=searchTxt)))
    response = self.__browser.response().read()

    links = BeautifulSoup.SoupStrainer('a', href=re.compile('descargar'), title=re.compile(searchTxt, flags=re.I))
    links = BeautifulSoup.BeautifulSoup(response, parseOnlyThese=links)
    for link in links:
      # not a valid link
      if not link.has_key('href'):
        continue
      if not link.has_key('title'):
        continue
      # no content in the link
      if not link.contents:
        continue
    
      title = link['title'].strip().split(None, 1)[1]  # .encode(soup.originalEncoding)
      title = title[title.lower().index(searchTxt.lower()):]
      url = link['href'].strip()

      filename = '%s.torrent' % (title, )

      if not download_all:
        print '[*] Found:', filename
        print '  [d] download'
        print '  [a] all'
        print '  [q] quit'
        ans = raw_input('> ')
      else:
        self.__download_link(url, output_dir, filename)
        ans = None

      if ans:
        if ans[0] in ('d', 'a'):
          download_all = (ans[0] == 'a')
          self.__download_link(url, output_dir, filename)
        elif ans[0] == 'q':
          break

    print '[*] Finished'


if __name__ == '__main__':
  if len(sys.argv) > 2:
    print 'Usage: %s [search_txt]'
    sys.exit(1)

  output_dir = '.'
  try:
    search_txt = sys.argv[1]
  except IndexError:
    search_txt = None

  browser = Browser()
  browser.enumerate_links(output_dir, search_txt)

