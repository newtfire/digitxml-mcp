<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    2026-04-09 syllabubFix.xsl
    Authored by: ebb + Claude (Anthropic)
    Purpose: Corrects four schema validation errors in syllabubRecipe.xml:
      1. Renames <it> element to <item> (lines 29x2)
      2. Renames misspelled attribute qant to quant (line 31)
      3. Adds missing required num="7" attribute to the Decorate <step> (line 63)
    Input:  data/syllabubRecipe.xml
    Output: outputs/syllabubRecipe.xml
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">

    <!-- Identity transform: copy everything through unchanged by default -->
    <xsl:mode on-no-match="shallow-copy"/>

    <!-- Fix 1: Rename <it> to <item> -->
    <xsl:template match="it">
        <item>
            <xsl:apply-templates select="@* | node()"/>
        </item>
    </xsl:template>

    <!-- Fix 2: Rename attribute qant to quant -->
    <xsl:template match="@qant">
        <xsl:attribute name="quant" select="."/>
    </xsl:template>

    <!-- Fix 3: Add missing num="7" to the unnumbered step -->
    <xsl:template match="step[not(@num)]">
        <step num="7">
            <xsl:apply-templates select="@* | node()"/>
        </step>
    </xsl:template>

</xsl:stylesheet>