#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

__pychecker__ = 'no-callinit no-classattr'


import BeautifulSoup
import mechanize
import multiprocessing
import os
import re
import shutil
import sys
import uuid
import urllib
import urllib2
import urlparse
import zipfile


DEST_PATH = '/data/store/Manga/'


class Browser(object):

  def __init__(self):
    object.__init__(self)
    self.__base_url = 'http://www.rom-world.com/'
    self.__browser = mechanize.Browser()
    self.__browser.set_handle_robots(False)
    self.__browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  def download(self, args):
    page_url, chapter_dir = args

    self.__browser.open(page_url)
    soup = BeautifulSoup.BeautifulSoup(self.__browser.response().read())
    links = soup('img', id='manga-page')

    assert len(links) == 1, 'Malformed url page %s' % page_url

    url = links[0]['src']
    output_path = os.path.join(chapter_dir, url.rsplit('/', 1)[1])

    if os.path.exists(output_path):
      print '[*] %s already downloaded' % (output_path, )
      return

    print '[*] Retrieving %s img to %s' % (page_url, output_path)
    urllib.urlretrieve(url, output_path)
    print '[*] %s successfully downloaded' % (page_url, )

  def zipit(self, chapter_name, chapter_dir, tasks):
    output_path = os.path.join(DEST_PATH, '%s.cbz' % chapter_name)
    if os.path.exists(output_path):
      print '[*] %s already there' % (output_path, )
      return

    map(self.download, tasks)
    cbz = zipfile.ZipFile(os.path.join(DEST_PATH, '%s.cbz' % chapter_name), 'w')
    for filename in os.listdir(chapter_dir):
      cbz.write(os.path.join(chapter_dir, filename))
    cbz.close()
    shutil.rmtree(chapter_dir)

  def enumerate_links(self, input_url):
    self.__browser.open(input_url)

    chapter_name = self.__browser.title().split(' - ', 1)[0]
    chapter_dir = os.path.join(DEST_PATH, chapter_name)
    try:
      os.mkdir(chapter_dir)
    except OSError:
      pass

    soup = BeautifulSoup.BeautifulSoup(self.__browser.response().read())
    o = urlparse.urlsplit(input_url)
    href_re = re.compile('/'.join(o.path.split('/')[2:-1]))
    links = soup('a', href=href_re)

    o = urlparse.urlsplit(links[1]['href'])
    start_dir_path, start_page = o.path.rsplit('/', 1)
    start_page = int(start_page)
    o = urlparse.urlsplit(links[-3]['href'])
    end_dir_path, end_page = o.path.rsplit('/', 1)
    end_page = int(end_page)
    assert start_dir_path == end_dir_path, 'Start and end dir paths differ'
    dir_path = start_dir_path

    tasks = []
    for page_idx in xrange(start_page, end_page + 1):
      page_url = urlparse.urlunsplit((o[0], o[1],
          '/'.join((dir_path, str(page_idx))), o[3], o[4]))
      tasks.append((page_url, chapter_dir))

    self.zipit(chapter_name, chapter_dir, tasks)

    print '[*] Finished'


if __name__ == '__main__':
  if len(sys.argv) == 1:
    print "Usage: %s <start_page>" % sys.argv[0]
    sys.exit(1)

  browser = Browser()
  for input_url in sys.argv[1:]:
    browser.enumerate_links(input_url)

