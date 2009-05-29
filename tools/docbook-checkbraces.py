#!/usr/bin/env python

import sys, xml.dom.minidom, re

assert(len(sys.argv) >= 2)

hasError = False
for filename in sys.argv[1:] :
	file = open(filename)
	input = file.read()
	file.close()

	leftCount = input.count("(") - input.count(":(")
	rightCount = input.count(")") - input.count(":)")
	if leftCount != rightCount :
		print filename + ": '(',')' brace mismatch: " + str(leftCount) + " != " + str(rightCount)
		hasError = True

	extraRightSquareBraces = 0
	if filename == "practical.xml" :
		extraRightSquareBraces = 1
	if input.count("[") != (input.count("]") - extraRightSquareBraces) :
		print filename + ": '[' brace mismatch: " + str(input.count("[")) + " != " + str(input.count("]") - extraRightSquareBraces)
		hasError = True

if hasError :
	sys.exit(1)
