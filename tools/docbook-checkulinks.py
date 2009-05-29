#!/usr/bin/env python

import urllib2, sys, xml.dom.minidom, xml.sax, os.path

assert(len(sys.argv) >= 2)

# Parse all files
urls = set()
for filename in sys.argv[1:] :
  try :
    file = open(filename)
    document = xml.dom.minidom.parseString(file.read())
  except IOError:
    continue
  except xml.parsers.expat.ExpatError:
    continue
  finally :
    file.close()
  ulinks = document.getElementsByTagName("ulink")
  for ulink in ulinks :
		url = ulink.getAttribute("url")
		if url == "xmpp.org" :
			continue
		urls.add(url)

# Test all urls
allOk = True
for url in urls :
	#print url
	try :
		response = urllib2.urlopen(url)
	except urllib2.URLError, e :
		print "Error opening " + url + ": " + str(e)
		allOk = False

if not allOk :
	sys.exit(-1)
