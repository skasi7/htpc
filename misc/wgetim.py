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
import urllib2
import urlparse

"""
        br.submit()

        cookiejar = br._ua_handlers["_cookies"].cookiejar

        # Add cookiejar to our requests session
        task.requests.add_cookiejar(cookiejar)
        # Add handler to urllib2 default opener for backwards compatibility
        handler = urllib2.HTTPCookieProcessor(cookiejar)
        if urllib2._opener:
            log.debug('Adding HTTPCookieProcessor to default opener')
            urllib2._opener.add_handler(handler)
        else:
            log.debug('Creating new opener and installing it')
            urllib2.install_opener(urllib2.build_opener(handler))
"""

###
# UTILITY
###
def is_valid_link(link):
  return link.has_key('href') and link.contents

def get_base_url(url):
  parts = urlparse.urlsplit(url)
  parts = (parts.scheme, parts.netloc, "", "", "")
  return urlparse.urlunsplit(parts)

def log(msg):
  print '[*] %s' % (msg, )

###
# INPUTS
###
def simple_link_input(url_iterable, *args, **kwargs):
  for url in url_iterable:
    base_url = get_base_url(url)
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url).read())
    links = [l for l in soup('a', *args, **kwargs)
        if is_valid_link(l)]
    for link in links:
      title = link.text.strip()
      href = urlparse.urljoin(base_url, link['href'].strip())
      yield href

###
# FILTERS
###
def interactive_filter(url_iterable):
  for url in url_iterable:
    print 'Url found: %s' % url
    ans = raw_input('Do you want to download it? ' '[y/N/q]')
    if not ans:
      continue
    elif ans[0] == 'y':
      yield url
    elif ans[0] == 'q':
      break

def remember_last_seen_filter(url_iterable, filename='.last_seen'):
  try:
    last_seen = open(filename, 'rb').read().strip()
  except IOError:
    last_seen = None
  first_seen = None
  for url in url_iterable:
    if url == last_seen:
      log('Last seen reached')
      break
    if first_seen is None:
      first_seen = url
    yield url
  if first_seen is not None:
    log('Remembering %s as last seen' % (first_seen, ))
    open(filename, 'wb').write(first_seen.strip())

def head_filter(url_iterable, n=10):
  _n = n
  for url in url_iterable:
    yield url
    _n -= 1
    if _n == 0:
      log('Head filter stopped after %d entries' % (n, ))
      break

###
# TRANSFORMATION
###
def romworld_transform(url_iterable):
  for url in url_iterable:
    soup = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url).read())
    links = soup('a', href=re.compile('games'))
    if len(links) != 1 or not is_valid_link(links[0]):
      continue
    new_url = links[0]['href']
    log('Url %s transformed to %s' % (url, new_url))
    yield new_url

###
# DOWNLOAD
###
def parallel_download(url_iterable, processes=None):
  def log_thread():
    while True:
      try:
        print stdout_queue.get()
        stdout_queue.task_done()
      except EOFError:
        break

  def _log(msg):
    stdout_queue.put(msg)

  def f(url):
    output_path = os.path.join(DEST_PATH, os.path.basename(url))
    if os.path.exists(output_path):
      _log('%s already present' % (output_path, ))
      return
    urllib.urlretrieve(url, output_path)
    _log('%s downloaded to %s' % (url, output_path))

  manager = multiprocessing.Manager()
  stdout_queue = manager.Queue()
  multiprocessing.Process(target=log_thread).start()
  _log('Log worker created!')
  workers = processes or multiprocessing.cpu_count()
  pool = multiprocessing.Pool(workers)
  _log('Download pool of %d workers created!' % (workers, ))
  pool.map_async(f, url_iterable)
  pool.close();
  pool.join();


if __name__ == '__main__':
  input_iterable = simple_link_input(['http://www.rom-world.com/'],
      href=re.compile('file.php'))
  filtered_iterable = head_filter(input_iterable, 1)
  transformed_iterable = romworld_transform(filtered_iterable)
  parallel_download(transformed_iterable)

