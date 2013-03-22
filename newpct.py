#!/usr/bin/python2.6
#-*- coding: utf-8 -*-

__pychecker__ = 'no-callinit no-classattr'


import mechanize
import os
import re
import sys
import uuid
import xml.parsers.expat


class RSSParser(object):

  def __init__(self):
    object.__init__(self)
    self.__element = None
    self.__links = None

  def __start_element(self, name, attrs):
    attrs = (attrs, )
    self.__element.append(name)

  def __end_element(self, name):
    if self.__element[-1] == name:
      self.__element.pop()

  def __char_data(self, data):
    if 'item' not in self.__element or self.__element[-1] != 'link':
      return
    if data.find('serie') == -1:
      return
    self.__links.append(data)

  def parse(self, data):
    self.__element = list()
    self.__links = list()
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = self.__start_element
    p.EndElementHandler = self.__end_element
    p.CharacterDataHandler = self.__char_data
    p.Parse(data)

  def links(self):
    return self.__links


class Browser(object):

  def __init__(self):
    object.__init__(self)
    self.__browser = mechanize.Browser()
    self.__log_in()

  def __log_in(self):
    self.__browser.open('http://www.newpct.com')
    self.__browser.form = list(self.__browser.forms())[1]
    self.__browser.form['userName'] = 'bugmenot777'
    self.__browser.form['userPass'] = 'bugmenot777'
    self.__browser.submit()

  def download_link(self, url):
    self.__browser.open(url)
    # print self.__browser.response().read()

    try:
      link = self.__browser.find_link(url_regex=r'descargar\/torrent\/')
    except mechanize.LinkNotFoundError, e:
      print 'Error (link not found error): %s' % str(e)
      return False

    # print link.url
    self.__browser.follow_link(link)
    filename = '%s.torrent' % uuid.uuid4()
    fd = open(filename, 'w')
    fd.write(self.__browser.response().read())
    fd.close()
    print 'Success! Link %s saved at %s' % (url, filename)
    return True

if __name__ == '__main__':
  if len(sys.argv) == 0:
    print 'Usage: %s <url> [url] ...'
    sys.exit(1)

  browser = Browser()
  for url in sys.argv[1:]:
    browser.download_link(url)

