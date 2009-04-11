#!/usr/bin/env python
# coding=utf-8

# Takes a docbook file, and outputs its dependencies.
# Follows XIncludes as well.
#
# Author: Remko Tronçon

import urllib, sys, xml.dom.minidom, xml.sax, os.path

assert(len(sys.argv) == 2)

files = [sys.argv[1]]
dependencies = set()
while len(files) > 0 :
  # Parse document
  filename = files.pop()
  try :
    file = open(filename)
    document = xml.dom.minidom.parseString(file.read())
  except IOError:
    continue
  except xml.parsers.expat.ExpatError:
    continue
  finally :
    file.close()

  # Add XIncludes
  includes = document.getElementsByTagNameNS("http://www.w3.org/2001/XInclude", "include")
  for include in includes :
    include_file = include.getAttribute("href")
    dependencies.add(include_file)
    if include.getAttribute("parse") != "text" :
      files.append(include_file)

  # Add Imagedata
  imagedatas = document.getElementsByTagName("imagedata")
  for imagedata in imagedatas :
    dependencies.add(imagedata.getAttribute("fileref"))

print ' '.join(dependencies)
