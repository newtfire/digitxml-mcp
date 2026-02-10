<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">
    
    <!-- Identity template: copy everything by default -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Handle items with quantLow/quantHigh - rename to quantMin/quantMax -->
    <xsl:template match="item[@quantLow and @quantHigh]">
        <xsl:copy>
            <xsl:attribute name="quantMin" select="@quantLow"/>
            <xsl:attribute name="quantMax" select="@quantHigh"/>
            <xsl:apply-templates select="@* except (@quantLow, @quantHigh)"/>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Handle items with quant containing space-separated values -->
    <xsl:template match="item[@quant[contains(., ' ')]]">
        <xsl:copy>
            <xsl:variable name="tokens" select="tokenize(@quant, '\s+')"/>
            <xsl:attribute name="quantMin" select="$tokens[1]"/>
            <xsl:attribute name="quantMax" select="$tokens[2]"/>
            <xsl:apply-templates select="@* except @quant"/>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- Handle items with single quant value - keep as quantMin only -->
    <xsl:template match="item[@quant[not(contains(., ' '))]]">
        <xsl:copy>
            <xsl:attribute name="quantMin" select="@quant"/>
            <xsl:apply-templates select="@* except @quant"/>
            <xsl:apply-templates select="node()"/>
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>