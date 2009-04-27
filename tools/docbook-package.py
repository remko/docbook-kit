#!/usr/bin/env python
# coding=utf-8

# Takes a flat DocBook XML input file, and generates a tarbal for it.
# All figures referenced from the XML file are added to the tarball, using
# a normalized name (e.g. MyArticle-Figure-1.png)
#
# Author: Remko Tronçon


import sys, re, os.path, xml.dom.minidom, shutil

assert(len(sys.argv) == 3)

targetDir = sys.argv[2]
baseName = sys.argv[2]

# Parse document
file = open(sys.argv[1])
document = xml.dom.minidom.parseString(file.read())
file.close()

# Create the target dir
os.mkdir(targetDir)

# Initialize renames
fileRenames = {}

# Figures
figures = document.getElementsByTagName("figure")
currentFigure = 1
for figure in figures :
	imageDatas = figure.getElementsByTagName("imagedata")
	imageFiles = set()
	for imageData in imageDatas :
		imageFiles.add(imageData.getAttribute("fileref"))

	currentImageData = 1
	for imageFile in imageFiles :
		if len(imageFiles) == 1 :
			imageFileName = baseName + "-Figure-" + str(currentFigure) + os.path.splitext(imageFile)[1]
		else :
			imageFileName = baseName + "-Figure-" + str(currentFigure) + "_" + str(currentImageData) + os.path.splitext(imageFile)[1]
		fileRenames[imageFile] = imageFileName
		shutil.copyfile(imageFile, os.path.join(targetDir, imageFileName))
		currentImageData += 1
	currentFigure += 1

# Transform the document
inputFile = open(sys.argv[1])
outputFile = open(os.path.join(targetDir, baseName + ".xml"), "w")
for line in inputFile.readlines() :
	for (oldFile, newFile) in fileRenames.items() :
		line = re.sub("fileref=\"" + oldFile + "\"", "fileref=\""+ newFile + "\"", line)
	outputFile.write(line)
outputFile.close()
inputFile.close()
