#!/usr/bin/env python
# coding=utf-8

# Generates FOP font metrics for the given font file.
# Usage: generate-font-metrics.py <font-file> <fop-dir>
#
# Author: Remko Tronçon

import os, sys

assert(len(sys.argv) == 3)
file = sys.argv[1]
fopDir = sys.argv[2]

# Detect FOP installation
fopLibDir = os.path.join(fopDir, "lib")
fopJAR = os.path.join(fopDir, "build", "fop.jar")
avalonJAR = ""
commonsLoggingJAR = ""
commonsIOJAR = ""
xmlGraphicsCommonsJAR = ""
for lib in os.listdir(fopLibDir) :
  if not lib.endswith(".jar") :
    continue
  if lib.startswith("avalon-framework") :
    avalonJAR = os.path.join(fopLibDir, lib)
  elif lib.startswith("commons-logging") :
    commonsLoggingJAR = os.path.join(fopLibDir, lib)
  elif lib.startswith("commons-io") :
    commonsIOJAR = os.path.join(fopLibDir, lib)
  elif lib.startswith("xmlgraphics-commons") :
    xmlGraphicsCommonsJAR = os.path.join(fopLibDir, lib)

classpath = fopJAR + ":" + avalonJAR + ":" + commonsLoggingJAR + ":" + commonsIOJAR + ":" + xmlGraphicsCommonsJAR

if file.endswith(".pfm") :
  pfmReadCmd = "java -cp " + classpath + " org.apache.fop.fonts.apps.PFMReader -q "
  os.system(pfmReadCmd + " " + file + " " + file.replace("pfm", "xml"))
if file.endswith(".ttf") :
  ttfReadCmd = "java -cp " + classpath + " org.apache.fop.fonts.apps.TTFReader -q "
  os.system(ttfReadCmd + " " + file + " " + file.replace("ttf", "xml"))
