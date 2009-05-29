#!/usr/bin/env python
# coding=utf-8

import sys, xml.dom.minidom, os.path

allowedStraightQuotesInExamples = ["didn't", "it's", "Alice's", "Queen's", "I'm", "what's", "he's"]
assert(len(sys.argv) >= 2)

# Retrieve the text portion from an XML node
def getText(nodelist):
  rc = ""
  for node in nodelist:
    if node.nodeType in [node.TEXT_NODE, node.CDATA_SECTION_NODE]:
      rc += node.data
  return rc

hasError = False
for filename in sys.argv[1:] :
  try :
    file = open(filename)
    document = xml.dom.minidom.parseString(file.read())
    nodes = [document.documentElement]
    while len(nodes) > 0 :
      node = nodes.pop()
      nodeText = getText(node.childNodes)
      nodePrintText = nodeText.encode("utf-8")
      if not (node.nodeType == xml.dom.Node.ELEMENT_NODE and (node.tagName == "programlisting" or node.tagName == "literal")) :
        if nodeText.find("‘".decode("utf-8")) != -1 :
          quoteIndex = nodePrintText.find("‘")
          nodePrintText = nodePrintText[max(0,quoteIndex-10):quoteIndex+10]
          print filename + ": Curly open quote: ..." + nodePrintText + "..."
          hasError = True
          continue
        if "'" in nodeText :
          quoteIndex = nodePrintText.find("'")
          nodePrintText = nodePrintText[max(0,quoteIndex-10):quoteIndex+10]
          print filename + ": Straight ' quote: ..." + nodePrintText + "..."
          hasError = True
          continue
        if "\"" in nodeText :
          quoteIndex = nodePrintText.find("\"")
          nodePrintText = nodePrintText[max(0,quoteIndex-10):quoteIndex+10]
          print filename + ": Straight \" quote:  ..." + nodePrintText + "..."
          hasError = True
          continue
        nodes += node.childNodes
  except IOError:
    continue
  except xml.parsers.expat.ExpatError:
    continue
  finally :
    file.close()

if hasError :
  sys.exit(1)
