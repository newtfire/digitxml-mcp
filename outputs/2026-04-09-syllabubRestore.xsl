<?xml version="1.0" encoding="UTF-8"?>
<!-- 
    2026-04-09 syllabubRestore.xsl
    Authored by: ebb + Claude (Anthropic)
    Purpose: Reverse of syllabubFix.xsl. Restores the original validation errors
             in syllabubRecipe.xml so data/syllabubRecipe.xml remains a test fixture
             for Jingtrang/pyjing schema validation.
      1. Renames <item unit="fruit"> back to <it>
      2. Renames quant attribute back to qant on the caster sugar item
      3. Strips num attribute from the Decorate step (step 7)
    Input:  outputs/syllabubRecipe.xml (the corrected file)
    Output: data/syllabubRecipe.xml (restored to buggy original)
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">

    <xsl:mode on-no-match="shallow-copy"/>

    <!-- Restore <it> for the lemon ingredient -->
    <xsl:template match="item[@unit='fruit']">
        <it>
            <xsl:apply-templates select="@* | node()"/>
        </it>
    </xsl:template>

    <!-- Restore misspelled qant attribute on the caster sugar item -->
    <xsl:template match="item[@unit='ounce']/@quant">
        <xsl:attribute name="qant" select="."/>
    </xsl:template>

    <!-- Restore missing num on the Decorate step -->
    <xsl:template match="step[@num='7']">
        <step>
            <xsl:apply-templates select="node()"/>
        </step>
    </xsl:template>

</xsl:stylesheet>