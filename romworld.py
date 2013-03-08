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


DEST_PATH = '/data/store/Juegos/mame/roms/'


def is_valid(link):
  return link.has_key('href') and link.contents


def f(args):
  input_url, title, output_queue = args

  soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(input_url).read())
  links = soup('a', href=re.compile('games'))

  if len(links) != 1 or not is_valid(links[0]):
    output_queue.put('[*] More than one link, ignoring')
    return

  url = links[0]['href']
  output_path = os.path.join(DEST_PATH, os.path.basename(url))

  if os.path.exists(output_path):
    output_queue.put('[*] %s already downloaded' % (title, ))
    return

  output_queue.put('[*] Retrieving %s to %s' % (title, output_path))
  urllib.urlretrieve(url, output_path)
  output_queue.put('[*] %s successfully downloaded' % (title, ))


def g(output_queue):
  while True:
    try:
      print output_queue.get()
      output_queue.task_done
    except EOFError:
      break


class Browser(object):

  def __init__(self):
    object.__init__(self)
    self.__base_url = 'http://www.rom-world.com/'
    self.__browser = mechanize.Browser()

  def enumerate_links(self):
    manager = multiprocessing.Manager()

    output_queue = manager.Queue()
    print '[*] Creating log process'
    log = multiprocessing.Process(target=g, args=(output_queue, ))
    log.start()

    print '[*] Creating process pool of %d workers' % (multiprocessing.cpu_count(), )
    pool = multiprocessing.Pool()

    print '[*] Starting parallel processing'
    letters = ['0-9'] + [c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    for letter in letters:
      url = '%sdl.php?name=MAME&letter=%s' % (self.__base_url, letter)
      print '[*]'
      print '[*] Opening %s' % (url, )
      print '[*]'
      self.__browser.open(url)

      tasks = []

      soup = BeautifulSoup.BeautifulSoup(self.__browser.response().read())
      for link in soup('a', href=re.compile('file.php')):
        if not is_valid(link):
          continue

        title = link.text.strip()
        href = link['href'].strip()
        
        input_url = '%s%s' % (self.__base_url, href)

        tasks.append((input_url, title, output_queue))

      pool.map_async(f, tasks)

    pool.close();
    pool.join();

    print '[*] Finished'


if __name__ == '__main__':
  browser = Browser()
  browser.enumerate_links()

