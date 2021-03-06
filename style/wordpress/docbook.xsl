<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!-- Include other stylesheets -->
  <xsl:import href="../../../docbook/xsl/xhtml/docbook.xsl"/>
  <xsl:include href="../common/params.xsl" />
  <xsl:include href="../common/inline.xsl" />
  <xsl:include href="component.xsl" />
  <xsl:include href="titlepage.xsl" />
  <xsl:include href="sections.xsl" />

  <xsl:param name="pdf.url"/>
  <xsl:param name="pdf.icon"/>
  <xsl:param name="wordpress.dir">../../wordpress</xsl:param>

  <xsl:output method="xml" encoding="UTF-8" indent="no" omit-xml-declaration="yes"/>

  <xsl:param name="use.extensions" select="0"/>
  <xsl:param name="section.autolabel" select="'0'"/>

  <xsl:param name="generate.toc"/>

  <xsl:template match="*" mode="process.root">
    <xsl:variable name="doc" select="self::*"/>
    <xsl:processing-instruction name="php">
      require('<xsl:value-of select="$wordpress.dir"/>/wp-blog-header.php'); 
      class MyPost { var $post_title = "<xsl:apply-templates select="$doc" mode="object.title.markup.textonly"/>"; }
      $wp_query->is_home = false;
      $wp_query->is_single = true;
      $wp_query->queried_object = new MyPost();
      get_header();
    </xsl:processing-instruction>
    <div id="content" class="narrowcolumn" role="main">
      <xsl:apply-templates select="."/>
    </div>
    <xsl:processing-instruction name="php">
      get_sidebar(); 
      get_footer(); 
    </xsl:processing-instruction>
  </xsl:template>
</xsl:stylesheet> 

