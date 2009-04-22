#
# Makefile include for a DocBook project.
#
# Make sure the variable DOCUMENT is set to the toplevel DocBook XML file
# before including the Makefile.
#
# Remko Tronçon
#

################################################################################
# Setup
################################################################################

DOCBOOKKIT_DIR ?= docbook-kit
DOCBOOK_XSL_DIR ?= docbook/xsl
DOCBOOK_XML_DIR ?= docbook/xml
DOCBOOK_DIR ?= docbook

################################################################################
# Sanity checks
################################################################################

ifndef DOCUMENT
$(error DOCUMENT variable not defined)
endif

################################################################################

DOCBOOK_CATALOG = $(DOCBOOK_XML_DIR)/catalog.xml
DOCBOOK_XSL_HTML = $(DOCBOOKKIT_DIR)/style/html/docbook.xsl
DOCBOOK_XSL_FO = $(DOCBOOKKIT_DIR)/style/fo/docbook.xsl
FONTS_DIR = $(DOCBOOKKIT_DIR)/fonts

PDFTK = $(shell which pdftk)
FOP = $(shell which fop)
FOP_DIR = $(dir $(FOP))

LIBXML_FLAGS = --nonet --xinclude
XSLTPROC_FLAGS = 

FOP_CONFIG_FILE = fop.cfg

################################################################################

export XML_CATALOG_FILES=$(DOCBOOK_CATALOG)
DOCUMENT_DEPENDENCIES = $(shell $(DOCBOOKKIT_DIR)/tools/docbook-deps.py $(DOCUMENT)) $(DOCBOOK_DIR)
TARGET_BASE = $(basename $(DOCUMENT))

ifneq ($(FOP),)
all: check-document $(TARGET_BASE).html $(TARGET_BASE).pdf
else
all: check-document $(TARGET_BASE).html
endif

.PHONY: clean
clean:
	-rm -f $(TARGET_BASE).pdf $(TARGET_BASE).fo $(TARGET_BASE).html $(TARGET_BASE).txt $(CLEANFILES)
	
.PHONY: html
html: $(TARGET_BASE).html

.PHONY: txt
txt: $(TARGET_BASE).txt

.PHONY: pdf
pdf: $(TARGET_BASE).pdf

$(TARGET_BASE).flat.xml: $(DOCUMENT) $(DOCUMENT_DEPENDENCIES)
	xmllint $(LIBXML_FLAGS) --postvalid $(DOCUMENT) > $@

$(TARGET_BASE).html: $(DOCUMENT) $(DOCUMENT_DEPENDENCIES) $(DOCBOOK_XSL_HTML)
	xsltproc $(XSLTPROC_FLAGS) $(LIBXML_FLAGS) $(DOCBOOK_XSL_HTML_PARAMS) --output $@ $(DOCBOOK_XSL_HTML) $(DOCUMENT)

$(TARGET_BASE).pdf: $(TARGET_BASE).fo $(FOP_CONFIG_FILE)
	$(FOP) -c $(FOP_CONFIG_FILE) $< $@
	@if [ "$(DOCUMENT_ATTACHMENTS)" ]; then \
		if [ -x "$(PDFTK)" -a "$DOCUMENT_ATTACHMENTS" ]; then \
			mv $(TARGET_BASE).pdf $(TARGET_BASE)_bare.pdf; \
			($(DOCBOOKKIT_DIR)/tools/docbook-pdfmetainfo.py $(DOCUMENT); $(PDFTK) $(TARGET_BASE)_bare.pdf dump_data) | $(PDFTK) $(TARGET_BASE)_bare.pdf update_info - output $(TARGET_BASE)_withinfo.pdf; \
			rm $(TARGET_BASE)_bare.pdf; \
			$(PDFTK) $(TARGET_BASE)_withinfo.pdf attach_files $(DOCUMENT_ATTACHMENTS) output $(TARGET_BASE).pdf compress; \
			rm $(TARGET_BASE)_withinfo.pdf; \
		else \
			echo "WARNING: PDFTK not found, not adding sources as attachments"; \
		fi \
	fi

$(TARGET_BASE).fo: $(DOCUMENT) $(DOCUMENT_DEPENDENCIES) $(DOCBOOK_XSL_FO)
	xsltproc $(XSLTPROC_FLAGS) $(LIBXML_FLAGS) -o $@ $(DOCBOOK_XSL_FO_PARAMS) $(DOCBOOK_XSL_FO) $(DOCUMENT)

$(TARGET_BASE).txt: $(TARGET_BASE).html
	links --dump 1 $< > $@

.PHONY: check-document
check-document: $(DOCUMENT) $(DOCUMENT_DEPENDENCIES)
	xmllint $(LIBXML_FLAGS) --postvalid --noout $(DOCUMENT)

################################################################################
# Fop files
################################################################################

$(FOP_CONFIG_FILE): 
	echo "<fop version=\"1.0\"><renderers><renderer mime=\"application/pdf\"><fonts><directory recursive=\"true\">$(FONTS_DIR)</directory></fonts></renderer></renderers></fop>" | xmllint --format - > $@

################################################################################
# Docbook
################################################################################

DOCBOOK_VERSION=4.4
DOCBOOK_XSL_VERSION=1.74.0

$(DOCBOOK_DIR): $(DOCBOOK_XML_DIR) $(DOCBOOK_XSL_DIR)

.PHONY: docbook-clean
docbook-clean:
	-rm -rf docbook

$(DOCBOOK_XML_DIR):
	-rm -f docbook-xml-$(DOCBOOK_VERSION).zip
	wget http://www.docbook.org/xml/$(DOCBOOK_VERSION)/docbook-xml-$(DOCBOOK_VERSION).zip
	mkdir -p $(DOCBOOK_XML_DIR)
	unzip -q docbook-xml-$(DOCBOOK_VERSION).zip -d $(DOCBOOK_XML_DIR)
	rm docbook-xml-$(DOCBOOK_VERSION).zip

$(DOCBOOK_XSL_DIR):
	-rm -f docbook-xsl-$(DOCBOOK_XSL_VERSION).zip
	wget http://dfn.dl.sourceforge.net/sourceforge/docbook/docbook-xsl-$(DOCBOOK_XSL_VERSION).zip
	unzip -q docbook-xsl-$(DOCBOOK_XSL_VERSION).zip
	mv docbook-xsl-$(DOCBOOK_XSL_VERSION) $(DOCBOOK_XSL_DIR)
	-rm -rf $(DOCBOOK_XSL_DIR)/epub $(DOCBOOK_XSL_DIR)/slides $(DOCBOOK_XSL_DIR)/website $(DOCBOOK_XSL_DIR)/xhtml $(DOCBOOK_XSL_DIR)/xhtml-1_1 $(DOCBOOK_XSL_DIR)/roundtrip $(DOCBOOK_XSL_DIR)/docsrc $(DOCBOOK_XSL_DIR)/eclipse $(DOCBOOK_XSL_DIR)/htmlhelp $(DOCBOOK_XSL_DIR)/javahelp $(DOCBOOK_XSL_DIR)/manpages $(DOCBOOK_XSL_DIR)/profiling $(DOCBOOK_XSL_DIR)/tools $(DOCBOOK_XSL_DIR)/tests
	rm docbook-xsl-$(DOCBOOK_XSL_VERSION).zip
