# The toplevel DocBook file of our project
# The toplevel document file
DOCUMENT = MyDocument.xml

# Attacments (Optional). These will be attached to the generated PDF.
# Requires 'pdftk'
DOCUMENT_ATTACHMENTS = MyAttachment.txt

# Include the DocBook Kit's makefile rules
include docbook-kit/tools/Makefile.inc

# If you have generated files, add custom rules for them
MyGeneratedFile.xml:
	echo "<para>This is a generated file</para>" > $@

CLEANFILES += MyGeneratedFile.xml
