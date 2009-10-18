<?xml version="1.0" encoding="ASCII"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" version="1.0">

<xsl:template match="article/title|article/articleinfo/title" mode="titlepage.mode" priority="2">
  <xsl:param name="node" select="ancestor::article[1]"/>

  <xsl:element name="h2" namespace="http://www.w3.org/1999/xhtml">
    <xsl:attribute name="class">title</xsl:attribute>
    <xsl:if test="$generate.id.attributes = 0">
      <xsl:call-template name="anchor">
        <xsl:with-param name="node" select="$node"/>
        <xsl:with-param name="conditional" select="0"/>
      </xsl:call-template>
    </xsl:if>
    <xsl:apply-templates select="$node" mode="object.title.markup">
      <xsl:with-param name="allow-anchors" select="1"/>
    </xsl:apply-templates>
    <xsl:if test="$pdf.url != ''">
      <xsl:text> </xsl:text>
      <xsl:choose>
        <xsl:when test="$pdf.icon = ''">
          <xsl:text>[</xsl:text>
          <xsl:element name="a" namespace="http://www.w3.org/1999/xhtml">
            <xsl:attribute name="href">
              <xsl:value-of select="$pdf.url"/>
            </xsl:attribute>
            <xsl:text>PDF</xsl:text>
          </xsl:element>
          <xsl:text>]</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:element name="a" namespace="http://www.w3.org/1999/xhtml">
            <xsl:attribute name="href">
              <xsl:value-of select="$pdf.url"/>
            </xsl:attribute>
            <xsl:element name="img" namespace="http://www.w3.org/1999/xhtml">
              <xsl:attribute name="src">
                <xsl:value-of select="$pdf.icon"/>
              </xsl:attribute>
            </xsl:element>
          </xsl:element>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
  </xsl:element>
</xsl:template>

</xsl:stylesheet>
