#!/usr/bin/env python
# coding=utf-8

# Generates meta info for a PDF from a DocBook document, which can be used 
# as input for PDFTK.
#
# Author: Remko Tronçon

import sys, xml.dom.minidom, os.path

def getText(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType == node.TEXT_NODE:
      rc += node.data
  return rc

assert(len(sys.argv) == 2)

file = open(sys.argv[1])
document = xml.dom.minidom.parseString(file.read())
file.close()

titles = document.getElementsByTagName("title")
if len(titles) > 0 :
  print "InfoKey: Title"
  print "InfoValue: " + getText(titles[0].childNodes).encode("utf-8")
authors = document.getElementsByTagName("author")
if len(authors) > 0 :
  author = ""
  firstNames = authors[0].getElementsByTagName("firstname")
  if len(firstNames) > 0 :
    author += " " + getText(firstNames[0].childNodes)
  surNames = authors[0].getElementsByTagName("surname")
  if len(surNames) > 0 :
    author += " " + getText(surNames[0].childNodes)
  author = author.strip()
  if author != "" :
    print "InfoKey: Author"
    print "InfoValue: " + author.encode("utf-8")
