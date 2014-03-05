#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

__pychecker__ = 'no-callinit no-classattr'


import BeautifulSoup
import mechanize
import multiprocessing
import os
import re
import sys
import uuid
import urllib
import urllib2


BASE_URL = 'http://www.mangatraders.com'
DEST_PATH = '/data/store/Manga/'


def f(task_queue, output_queue):
  while True:
    try:
      input_url = task_queue.get()
      output_queue.put('[*] Processing %s...' % input_url)

      soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(input_url).read())

      links = soup('input', value='Next Page')
      if len(links) != 1:
        output_queue.put('[*] More than one link, ignoring')
        continue

      next_page = '%s%s' % (BASE_URL, links[0]['onclick'].split('=', 1)[1][1:-1])
      task_queue.put(next_page)

      links = soup('option', selected='selected')
      if len(links) != 2:
        output_queue.put('[*] More than two options selected, ignoring')
        continue
      dst_path = os.path.join(DEST_PATH, links[0].string)
      if not os.path.isdir(dst_path):
        os.mkdir(dst_path)
      dst_filename = os.path.join(dst_path, os.path.split(links[1].string)[-1])

      links = soup('img', usemap='#imageMap')
      if len(links) != 1:
        output_queue.put('[*] More than one image, ignoring')
        continue
      image_url = links[0]['src']

      urllib.urlretrieve(image_url, dst_filename)
      output_queue.put('[*] Image %s saved to %s' % (image_url, dst_filename))
    except EOFError:
      break
  

def g(output_queue):
  while True:
    try:
      print output_queue.get()
      output_queue.task_done
    except EOFError:
      break


class Browser(object):

  def __init__(self, start_page):
    object.__init__(self)
    self.__start_page = start_page

  def enumerate_links(self):
    manager = multiprocessing.Manager()

    output_queue = manager.Queue()
    print '[*] Creating log process'
    log = multiprocessing.Process(target=g, args=(output_queue, ))
    log.start()

    task_queue = manager.Queue()
    print '[*] Creating process pool of %d workers' % (multiprocessing.cpu_count(), )
    pool = list()
    for _ in xrange(multiprocessing.cpu_count()):
      process = multiprocessing.Process(target=f, args=(task_queue, output_queue))
      pool.append(process)
      process.start()

    print '[*] Starting parallel processing'
    task_queue.put(self.__start_page)

    for process in pool:
        process.join()

    print '[*] Finished'


if __name__ == '__main__':
  if len(sys.argv) == 1:
    print "Usage: %s <start_page>" % sys.argv[0]
    sys.exit(1)
  browser = Browser(sys.argv[1])
  browser.enumerate_links()

