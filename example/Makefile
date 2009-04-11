# The toplevel DocBook file of our project
DOCUMENT = MyDocument.xml

# Include the DocBook Kit's makefile rules
include docbook-kit/tools/Makefile.inc

# If you have generated files, add custom rules for them
MyGeneratedFile.xml:
	echo "<para>This is a generated file</para>" > $@

CLEANFILES += MyGeneratedFile.xml
