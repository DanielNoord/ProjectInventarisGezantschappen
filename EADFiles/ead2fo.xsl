<?xml version="1.0" encoding="UTF-8"?>

<!--
ead2fo.xsl voor FOP
Stylesheet voor de omzetting van EAD 2002 naar PDF.

Ivo Zandhuis (ivo@zandhuis.nl)

*************
2004-09-21	Afvangen @audience
2004-08-03	Parametriseren onderdrukken van niet-openbare namen
						parameter $year (jaartal) voor jaar waarna een naam niet-openbaar is (default: 1894)
						parameter $in_or_external (internal | external) voor het vastleggen van in- of externe publicatie (default: internal)
2004-06-30	Aanpassing aanroepen van alle soorten inleidingen.
2004-06-30	Verwerking van [bibliography/title] verbeterd.
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:fox="http://xml.apache.org/fop/extensions">

<!-- parameters -->
		<xsl:param name="in_or_external">external</xsl:param>
		<xsl:param name="year">1894</xsl:param>

	<!-- Root -->
	<xsl:template match="/" name="make-inventaris">
	
		<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:fox="http://xml.apache.org/fop/extensions">
			
			<fo:layout-master-set>
				<fo:simple-page-master master-name="only" 
													page-height="29.7cm" page-width="21.0cm" 
													margin-right="2.5cm" margin-left="2.5cm" 
													margin-bottom="1cm" margin-top="1.5cm">
					<fo:region-body margin-top="2cm" margin-bottom="2cm"/>
					<fo:region-before extent="1cm"/> 
					<fo:region-after extent="1cm"/>
				</fo:simple-page-master>
			</fo:layout-master-set>
			
			<fo:page-sequence master-reference="only">
				<fo:flow flow-name="xsl-region-body">
					<!-- titelpagina -->
					<fo:table>
						<fo:table-column column-width="16cm"/>
						<fo:table-body>
							<fo:table-row height="4cm">
								<fo:table-cell>
									<fo:block text-align="end" font-size="20pt" font-weight="bold" space-after="100pt">
						                        <xsl:value-of select="/ead/eadheader/eadid"/>
									</fo:block>
								</fo:table-cell>
							</fo:table-row>
							<fo:table-row height="4cm">
								<fo:table-cell>
									<fo:block font-size="20pt">
										<xsl:value-of select="/ead/eadheader/filedesc/titlestmt/titleproper"/>
									</fo:block>
									<fo:block font-size="14pt">
										<xsl:value-of select="/ead/eadheader/filedesc/titlestmt/subtitle"/>
									</fo:block>
								</fo:table-cell>
							</fo:table-row>
							<fo:table-row>
								<fo:table-cell text-align="center" vertical-align="top">
									<fo:block>
										<xsl:if test="/ead/frontmatter">
											<fo:external-graphic height="10cm">
												<xsl:attribute name="src"><xsl:value-of select="/ead/frontmatter/p/extptr/@href"/></xsl:attribute>
											</fo:external-graphic>
										</xsl:if>
									</fo:block>
								</fo:table-cell>
							</fo:table-row>
							<fo:table-row height="2cm">
								<fo:table-cell vertical-align="bottom">
									<fo:block font-size="12pt">
										<xsl:value-of select="/ead/eadheader/filedesc/titlestmt/author"/>
									</fo:block>
									<fo:block font-size="12pt">
										<xsl:value-of select="/ead/eadheader/filedesc/titlestmt/sponsor"/>
									</fo:block>
									<fo:block font-size="12pt">
										<xsl:value-of select="/ead/eadheader/filedesc/publicationstmt/publisher"/>
										<xsl:if test="/ead/eadheader/filedesc/publicationstmt/date">
											<xsl:text>, </xsl:text>
											<xsl:value-of select="/ead/eadheader/filedesc/publicationstmt/date"/>
										</xsl:if>
									</fo:block>
								</fo:table-cell>
							</fo:table-row>
						</fo:table-body>
					</fo:table>
				</fo:flow>
			</fo:page-sequence>
	
			<fo:page-sequence master-reference="only">
				<fo:static-content flow-name="xsl-region-before">
						<fo:table>
							<fo:table-column column-width="6cm"/>
							<fo:table-column column-width="10cm"/>
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell>
										<fo:block font-size="8pt">
											<xsl:value-of select="ead/archdesc/did/repository"/>
										</fo:block>
									</fo:table-cell>
									<fo:table-cell>
										<fo:block font-size="8pt" text-align="end">
											<xsl:value-of select="ead/eadheader/eadid"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
								<fo:table-row>
									<fo:table-cell number-columns-spanned="2">
										<fo:block font-size="8pt">
											<xsl:value-of select="ead/eadheader/filedesc/titlestmt/titleproper[@type='short']"/>
										</fo:block>
									</fo:table-cell>
								</fo:table-row>
							</fo:table-body>
						</fo:table>
				</fo:static-content>
				<fo:static-content flow-name="xsl-region-after">
					<fo:block font-size="10pt" text-align="center">
					- <fo:page-number/> -	
					</fo:block>
					<xsl:if test="$in_or_external='internal'">
						<fo:block font-size="10pt" text-align="center">
						********************* ALLEEN VOOR INTERN GEBRUIK *********************
						</fo:block>					
					</xsl:if>
				</fo:static-content>
				<fo:flow flow-name="xsl-region-body">
					<xsl:apply-templates select="/ead/archdesc"/>
					<fo:block font-size="24pt" padding-after="1cm" break-before="page">
						Inhoudsopgave
					</fo:block>
					<fo:table>
						<fo:table-column column-width="15.5cm"/>
						<fo:table-column column-width="0.5cm"/>
						<fo:table-body>
							<xsl:apply-templates mode="toc"/>
						</fo:table-body>
					</fo:table>
					<xsl:apply-templates mode="pdf-toc" select="/ead/archdesc/did/head | /ead/archdesc/dsc/head"/>
				</fo:flow>
			</fo:page-sequence>
			
		</fo:root>
	</xsl:template>
	
	
	<!-- 
	
	
****************************** SAMENVATTING ********************************** 

-->
	<xsl:template match="archdesc/did">
		<!-- de high-level did wordt in een vastgestelde volgorde gepresenteerd op de eerste pagina -->
		<fo:block break-after="page">
			<xsl:apply-templates select="head"/>
			<fo:block space-before="20pt">
				<xsl:for-each select="unittitle">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="unitdate">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="unitid">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="container">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="physdesc">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="langmaterial">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="materialspec">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="repository">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="physloc">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="origination">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="dao">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="daogrp">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="abstract">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
				<xsl:for-each select="note">
					<xsl:apply-templates select="."/>
				</xsl:for-each>
			</fo:block>
		</fo:block>
	</xsl:template>
	<xsl:template match="    /ead/archdesc/did/abstract |
	                                       /ead/archdesc/did/container |
	                                       /ead/archdesc/did/dao |
	                                       /ead/archdesc/did/daogrp |
	                                       /ead/archdesc/did/langmaterial |
	                                       /ead/archdesc/did/materialspec |
	                                       /ead/archdesc/did/note |
	                                       /ead/archdesc/did/origination |
	                                       /ead/archdesc/did/physdesc |
	                                       /ead/archdesc/did/physloc |
	                                       /ead/archdesc/did/repository |
	                                       /ead/archdesc/did/unitdate |
	                                       /ead/archdesc/did/unitid |
	                                       /ead/archdesc/did/unittitle">
		<fo:block space-before="10pt" font-weight="bold">
			<xsl:value-of select="@label"/>
		</fo:block>
		<fo:block margin-left="1cm" font-size="10pt">
			<xsl:apply-templates/>
		</fo:block>
	</xsl:template>
	<!--

******************************** KOPJES *****************************

-->
	<xsl:template match="archdesc/did/head">
		<fo:block id="{generate-id()}" font-size="24pt" break-before="page">
			<xsl:apply-templates/>
		</fo:block>
	</xsl:template>

	<xsl:template match="head">
		<xsl:choose>
			<xsl:when test="count(ancestor::node()) = 6">
				<fo:block id="{generate-id()}" font-size="22pt" 
								padding-before="10pt" padding-after="10pt" 
								break-before="page" keep-with-next="1">
					<xsl:apply-templates/>
				</fo:block>
			</xsl:when>
			<xsl:when test="count(ancestor::node()) = 7">
				<fo:block id="{generate-id()}" font-size="18pt" 
								padding-before="10pt" padding-after="10pt" 
								keep-with-next="1">
					<xsl:apply-templates/>
				</fo:block>
			</xsl:when>
			<xsl:when test="count(ancestor::node()) = 8">
				<fo:block id="{generate-id()}" font-size="14pt" 
								padding-before="10pt" padding-after="10pt" 
								keep-with-next="1">
					<xsl:apply-templates/>
				</fo:block>
			</xsl:when>
			<xsl:otherwise>
				<fo:block id="{generate-id()}" font-size="12pt" 
								padding-before="10pt" padding-after="10pt" 
								font-weight="bold" keep-with-next="1">
					<xsl:apply-templates/>
				</fo:block>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	
	<xsl:template match="dsc/head" mode="keuze">
		<fo:table-row>
			<fo:table-cell number-columns-spanned="5">
				<fo:block id="{generate-id()}" font-size="24pt" break-before="page">
					<xsl:apply-templates/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
	</xsl:template>
	<!--

**************************************** teksten ************************************

-->

	<xsl:template match="//*[@id]">
		<fo:block id="{generate-id()}"/>
	</xsl:template>
	
	<xsl:template match="ref[@target]">
		<xsl:variable name="tar" select="@target"></xsl:variable>
		<fo:basic-link color="blue" internal-destination="{generate-id(//*[@id=$tar])}">
			<xsl:apply-templates></xsl:apply-templates>
		</fo:basic-link>		
	</xsl:template>

	<xsl:template match="p">
		<fo:block margin-left="2cm" text-align="left">
			<xsl:apply-templates/>
		</fo:block>
	</xsl:template>
	<xsl:template match="note/p | dsc//p">
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="archdesc/dsc">
		<fo:table>
			<fo:table-column column-width="2.5cm"/>
			<fo:table-column column-width="2cm"/>
			<fo:table-column column-width="2cm"/>
			<fo:table-column column-width="4cm"/>
			<fo:table-column column-width="5.5cm"/>
			<fo:table-body>
				<xsl:apply-templates mode="keuze"/>
			</fo:table-body>
		</fo:table>
	</xsl:template>
	<!-- rubrieksbeschrijving -->
	<xsl:template match="c01[@level='series'] | 
						       c02[@level='series'] | 
							c03[@level='series'] | 
							c04[@level='series'] | 
							c05[@level='series'] | 
							c06[@level='series'] | 
							c07[@level='series'] | 
							c08[@level='series'] | 
							c09[@level='series'] | 
							c10[@level='series'] | 
							c11[@level='series'] | 
							c12[@level='series'] | 
							c[@level='series'] |
	                              c01[@level='subseries'] | 
						     c02[@level='subseries'] | 
							c03[@level='subseries'] | 
							c04[@level='subseries'] | 
							c05[@level='subseries'] | 
							c06[@level='subseries'] | 
							c07[@level='subseries'] | 
							c08[@level='subseries'] | 
							c09[@level='subseries'] | 
							c10[@level='subseries'] | 
							c11[@level='subseries'] | 
							c12[@level='subseries'] | 
							c[@level='subseries'] |
	                              c01[@level='subfonds'] | 
						     c02[@level='subfonds'] | 
							c03[@level='subfonds'] | 
							c04[@level='subfonds'] | 
							c05[@level='subfonds'] | 
							c06[@level='subfonds'] | 
							c07[@level='subfonds'] | 
							c08[@level='subfonds'] | 
							c09[@level='subfonds'] | 
							c10[@level='subfonds'] | 
							c11[@level='subfonds'] | 
							c12[@level='subfonds'] | 
							c[@level='subfonds']" mode="keuze">
		<fo:table-row keep-with-next="1">
			<fo:table-cell padding-before="15pt">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="4" padding-before="15pt">
				<xsl:apply-templates select="did"></xsl:apply-templates>
				<fo:block id="{generate-id()}" font-style="italic">
					<xsl:apply-templates select="did/unitid"/>
					<xsl:text> </xsl:text>
					<xsl:apply-templates select="did/unittitle"/>
				</fo:block>
				<fo:block> 
					<xsl:text> </xsl:text>
					<xsl:apply-templates select="did/unitdate"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="keuze"/>
	</xsl:template>
	<!-- verzamelbeschrijving -->
	<xsl:template match="	c01[@otherlevel='filegrp'] | 
									c02[@otherlevel='filegrp'] | 
									c03[@otherlevel='filegrp'] | 
									c04[@otherlevel='filegrp'] | 
									c05[@otherlevel='filegrp'] | 
									c06[@otherlevel='filegrp'] | 
									c07[@otherlevel='filegrp'] | 
									c08[@otherlevel='filegrp'] | 
									c09[@otherlevel='filegrp'] | 
									c10[@otherlevel='filegrp'] | 
									c11[@otherlevel='filegrp'] | 
									c12[@otherlevel='filegrp'] | 
									c[@otherlevel='filegrp']" mode="keuze">
		<fo:table-row keep-with-next="1">
			<fo:table-cell padding-before="8pt">
				<xsl:apply-templates select="did"></xsl:apply-templates>
				<fo:block id="{generate-id()}">
					<xsl:apply-templates select="did/unitid"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="4" padding-before="8pt">
				<fo:block>
					<xsl:apply-templates select="did/unittitle"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<fo:table-row>
			<fo:table-cell>
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="3">
				<fo:block>
					<xsl:apply-templates select="did/unitdate"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell>
				<fo:block text-align="end">
					<xsl:apply-templates select="did/physdesc"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="verzamel"/>
	</xsl:template>
	<!-- verzamelbeschrijving -->
	<xsl:template match="	c01[@otherlevel='filegrp'] | 
									c02[@otherlevel='filegrp'] | 
									c03[@otherlevel='filegrp'] | 
									c04[@otherlevel='filegrp'] | 
									c05[@otherlevel='filegrp'] | 
									c06[@otherlevel='filegrp'] | 
									c07[@otherlevel='filegrp'] | 
									c08[@otherlevel='filegrp'] | 
									c09[@otherlevel='filegrp'] | 
									c10[@otherlevel='filegrp'] | 
									c11[@otherlevel='filegrp'] | 
									c12[@otherlevel='filegrp'] | 
									c[@otherlevel='filegrp']" mode="verzamel">
		<fo:table-row keep-with-next="1">
			<fo:table-cell>
				<fo:block></fo:block>
			</fo:table-cell>
			<fo:table-cell padding-before="8pt">
				<xsl:apply-templates select="did"></xsl:apply-templates>
				<fo:block id="{generate-id()}">
					<xsl:apply-templates select="did/unitid"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="3" padding-before="8pt">
				<fo:block>
					<xsl:apply-templates select="did/unittitle"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<fo:table-row>
			<fo:table-cell number-columns-spanned="2">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="2">
				<fo:block>
					<xsl:apply-templates select="did/unitdate"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell>
				<fo:block text-align="end">
					<xsl:apply-templates select="did/physdesc"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="verzamel2"/>
	</xsl:template>
	<!-- enkelvoudige beschrijving -->
	<xsl:template match="
									c01[@level='file'] |
									c02[@level='file'] | 
									c03[@level='file'] | 
									c04[@level='file'] | 
									c05[@level='file'] | 
									c06[@level='file'] | 
									c07[@level='file'] | 
									c08[@level='file'] | 
									c09[@level='file'] | 
									c10[@level='file'] | 
									c11[@level='file'] | 
									c12[@level='file'] |
									c[@level='file']" mode="keuze">
		<fo:table-row keep-with-next="1">
			<fo:table-cell padding-before="8pt">
				<xsl:apply-templates select="did"></xsl:apply-templates>
				<fo:block id="{generate-id()}" color="red">
					<xsl:apply-templates select="did/unitid"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="4" padding-before="8pt" keep-together="1">
				<fo:block>
					<xsl:apply-templates select="did/unittitle"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<fo:table-row>
			<fo:table-cell>
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="3">
				<fo:block>
					<xsl:apply-templates select="did/unitdate"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell>
				<fo:block text-align="end">
					<xsl:apply-templates select="did/physdesc"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="enkel"/>
	</xsl:template>
	<!-- deelbeschrijving -->
	<xsl:template match="
									c01[@level='file'] |
									c02[@level='file'] | 
									c03[@level='file'] | 
									c04[@level='file'] | 
									c05[@level='file'] | 
									c06[@level='file'] | 
									c07[@level='file'] | 
									c08[@level='file'] | 
									c09[@level='file'] | 
									c10[@level='file'] | 
									c11[@level='file'] | 
									c12[@level='file'] |
									c[@level='file']" mode="verzamel">
		<fo:table-row>
			<fo:table-cell>
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell>
				<xsl:apply-templates select="did"></xsl:apply-templates>
				<fo:block id="{generate-id()}" color="red">
					<xsl:apply-templates select="did/unitid"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="3" keep-together="1">
				<fo:block>
					<xsl:apply-templates select="did/unittitle"/>
					<xsl:if test="did/unitdate">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/unitdate"/>
					</xsl:if>
					<xsl:if test="did/physdesc">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/physdesc"/>
					</xsl:if>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="deel"/>
	</xsl:template>
	<!-- deelbeschrijving -->
	<xsl:template match="
									c01[@level='file'] |
									c02[@level='file'] | 
									c03[@level='file'] | 
									c04[@level='file'] | 
									c05[@level='file'] | 
									c06[@level='file'] | 
									c07[@level='file'] | 
									c08[@level='file'] | 
									c09[@level='file'] | 
									c10[@level='file'] | 
									c11[@level='file'] | 
									c12[@level='file'] |
									c[@level='file']" mode="verzamel2">
		<fo:table-row>
			<fo:table-cell number-columns-spanned="2">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell>
				<xsl:apply-templates select="did"></xsl:apply-templates>
				<fo:block id="{generate-id()}" color="red">
					<xsl:apply-templates select="did/unitid"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="2" keep-together="1">
				<fo:block>
					<xsl:apply-templates select="did/unittitle"/>
					<xsl:if test="did/unitdate">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/unitdate"/>
					</xsl:if>
					<xsl:if test="did/physdesc">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/physdesc"/>
					</xsl:if>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="deel"/>
	</xsl:template>
	<xsl:template match="	c01[@level='item'] | 
									c02[@level='item'] | 
									c03[@level='item'] | 
									c04[@level='item'] | 
									c05[@level='item'] | 
									c06[@level='item'] | 
									c07[@level='item'] | 
									c08[@level='item'] | 
									c09[@level='item'] | 
									c10[@level='item'] | 
									c11[@level='item'] | 
									c12[@level='item'] | 
									c[@level='item'] |
									c01[@otherlevel='subfile'] | 
									c02[@otherlevel='subfile'] | 
									c03[@otherlevel='subfile'] | 
									c04[@otherlevel='subfile'] | 
									c05[@otherlevel='subfile'] | 
									c06[@otherlevel='subfile'] | 
									c07[@otherlevel='subfile'] | 
									c08[@otherlevel='subfile'] | 
									c09[@otherlevel='subfile'] | 
									c10[@otherlevel='subfile'] | 
									c11[@otherlevel='subfile'] | 
									c12[@otherlevel='subfile'] | 
									c[@otherlevel='subfile']" mode="deel">
		<fo:table-row>
			<fo:table-cell number-columns-spanned="2">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="3" keep-together="1">
				<fo:block>
					<xsl:if test="did/unitid">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/unitid"/>
					</xsl:if>
					<xsl:if test="did/unittitle">
						<xsl:text> </xsl:text>
					<xsl:apply-templates select="did/unittitle"/>
					</xsl:if>
					<xsl:if test="did/unitdate">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/unitdate"/>
					</xsl:if>
					<xsl:if test="did/physdesc">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/physdesc"/>
					</xsl:if>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="deel"/>
	</xsl:template>
	<xsl:template match="	c01[@level='item'] | 
									c02[@level='item'] | 
									c03[@level='item'] | 
									c04[@level='item'] | 
									c05[@level='item'] | 
									c06[@level='item'] | 
									c07[@level='item'] | 
									c08[@level='item'] | 
									c09[@level='item'] | 
									c10[@level='item'] | 
									c11[@level='item'] | 
									c12[@level='item'] | 
									c[@level='item'] |
									c01[@otherlevel='subfile'] | 
									c02[@otherlevel='subfile'] | 
									c03[@otherlevel='subfile'] | 
									c04[@otherlevel='subfile'] | 
									c05[@otherlevel='subfile'] | 
									c06[@otherlevel='subfile'] | 
									c07[@otherlevel='subfile'] | 
									c08[@otherlevel='subfile'] | 
									c09[@otherlevel='subfile'] | 
									c10[@otherlevel='subfile'] | 
									c11[@otherlevel='subfile'] | 
									c12[@otherlevel='subfile'] | 
									c[@otherlevel='subfile']" mode="enkel">
		<fo:table-row>
			<fo:table-cell number-columns-spanned="2">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="3" keep-together="1">
				<fo:block>
					<xsl:if test="did/unitid">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/unitid"/>
					</xsl:if>
					<xsl:if test="did/unittitle">
						<xsl:text> </xsl:text>
					<xsl:apply-templates select="did/unittitle"/>
					</xsl:if>
					<xsl:if test="did/unitdate">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/unitdate"/>
					</xsl:if>
					<xsl:if test="did/physdesc">
						<xsl:text> </xsl:text>
						<xsl:apply-templates select="did/physdesc"/>
					</xsl:if>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
		<xsl:apply-templates mode="enkel"/>
	</xsl:template>
	<xsl:template match="dsc//accessrestrict |
    										dsc//accruals |
    										dsc//acqinfo |
    										dsc//altformavail |
    										dsc//appraisal |
    										dsc//arrangement |
    										dsc//bibliography |
    										dsc//bioghist |
    										dsc//controlaccess |
    										dsc//custodhist |
    										dsc//fileplan |
    										dsc//index |
    										dsc//odd |
    										dsc//originalsloc |
    										dsc//otherfindaid |
    										dsc//phystech |
    										dsc//prefercite |
    										dsc//processinfo |
    										dsc//relatedmaterial |
    										dsc//scopecontent |
    										dsc//separatedmaterial |
    										dsc//userestrict" mode="keuze">
		<fo:table-row keep-with-previous="1">
			<fo:table-cell padding-after="8pt">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="4" padding-after="8pt">
				<fo:block font-size="9pt">
					<xsl:apply-templates/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
	</xsl:template>
	<xsl:template match="dsc//accessrestrict |
    										dsc//accruals |
    										dsc//acqinfo |
    										dsc//altformavail |
    										dsc//appraisal |
    										dsc//arrangement |
    										dsc//bibliography |
    										dsc//bioghist |
    										dsc//controlaccess |
    										dsc//custodhist |
    										dsc//fileplan |
    										dsc//index |
    										dsc//odd |
    										dsc//originalsloc |
    										dsc//otherfindaid |
    										dsc//phystech |
    										dsc//prefercite |
    										dsc//processinfo |
    										dsc//relatedmaterial |
    										dsc//scopecontent |
    										dsc//separatedmaterial |
    										dsc//userestrict" mode="verzamel">
		<fo:table-row keep-with-previous="1">
			<fo:table-cell padding-after="8pt">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="4" padding-after="8pt">
				<fo:block font-size="9pt">
					<xsl:apply-templates/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
	</xsl:template>
	<xsl:template match="dsc//accessrestrict |
    										dsc//accruals |
    										dsc//acqinfo |
    										dsc//altformavail |
    										dsc//appraisal |
    										dsc//arrangement |
    										dsc//bibliography |
    										dsc//bioghist |
    										dsc//controlaccess |
    										dsc//custodhist |
    										dsc//fileplan |
    										dsc//index |
    										dsc//odd |
    										dsc//originalsloc |
    										dsc//otherfindaid |
    										dsc//phystech |
    										dsc//prefercite |
    										dsc//processinfo |
    										dsc//relatedmaterial |
    										dsc//scopecontent |
    										dsc//separatedmaterial |
    										dsc//userestrict" mode="enkel">
		<fo:table-row keep-with-previous="1">
			<fo:table-cell padding-after="8pt">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="4" padding-after="8pt">
				<fo:block font-size="9pt">
					<xsl:apply-templates/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
	</xsl:template>
	<xsl:template match="dsc//accessrestrict |
    										dsc//accruals |
    										dsc//acqinfo |
    										dsc//altformavail |
    										dsc//appraisal |
    										dsc//arrangement |
    										dsc//bibliography |
    										dsc//bioghist |
    										dsc//controlaccess |
    										dsc//custodhist |
    										dsc//fileplan |
    										dsc//index |
    										dsc//odd |
    										dsc//originalsloc |
    										dsc//otherfindaid |
    										dsc//phystech |
    										dsc//prefercite |
    										dsc//processinfo |
    										dsc//relatedmaterial |
    										dsc//scopecontent |
    										dsc//separatedmaterial |
    										dsc//userestrict" mode="deel">
		<fo:table-row keep-with-previous="1">
			<fo:table-cell number-columns-spanned="2" padding-after="8pt">
				<fo:block> </fo:block>
			</fo:table-cell>
			<fo:table-cell number-columns-spanned="3" padding-after="8pt">
				<fo:block font-size="9pt">
					<xsl:apply-templates/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
	</xsl:template>
	<xsl:template match="title">
		<fo:inline font-style="italic">
			<xsl:apply-templates/>
		</fo:inline>
	</xsl:template>
	<xsl:template match="bibliography/bibref | bibliography/title">
		<fo:block margin-left="2cm" text-align="left">
			<xsl:apply-templates/>
		</fo:block>
	</xsl:template>
	<xsl:template match="list">
		<xsl:variable name="numtype">
			<xsl:choose>
				<xsl:when test="@numeration='arabic'">1</xsl:when>
				<xsl:when test="@numeration='upperalpha'">A</xsl:when>
				<xsl:when test="@numeration='loweralpha'">a</xsl:when>
				<xsl:when test="@numeration='upperroman'">I</xsl:when>
				<xsl:when test="@numeration='lowerroman'">i</xsl:when>
				<xsl:otherwise>1</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<fo:list-block provisional-distance-between-starts="18pt" provisional-label-separation="3pt">
			<xsl:for-each select="item">
				<fo:list-item>
					<fo:list-item-label end-indent="label-end()">
						<fo:block>
							<xsl:number count="item" level="single" from="list" format="{$numtype}"/>
							<xsl:text>.</xsl:text>
						</fo:block>
					</fo:list-item-label>
					<fo:list-item-body start-indent="body-start()">
						<fo:block>
							<xsl:apply-templates/>
						</fo:block>
					</fo:list-item-body>
				</fo:list-item>
			</xsl:for-each>
		</fo:list-block>
	</xsl:template>
	<xsl:template match="note">
		<fo:footnote>
			<fo:inline font-size="6pt" vertical-align="super">
				<xsl:number count="note" level="any" from="/ead/archdesc"/>
			</fo:inline>
			<fo:footnote-body>
				<fo:block space-before="12pt" font-size="8pt" margin-left="2cm">
					<fo:inline font-size="6pt" vertical-align="super">
						<xsl:number count="note" level="any" from="/ead/archdesc"/>
					</fo:inline>
					<xsl:text/>
					<xsl:apply-templates/>
				</fo:block>
			</fo:footnote-body>
		</fo:footnote>
	</xsl:template>
	
	<!-- 
	
		
	************************* INHOUDSOPGAVE *********************************
	
	-->
	
	<xsl:template match="head" mode="toc">
		<fo:table-row>
			<xsl:choose>
				<xsl:when test="count(ancestor::node()) = 4">
					<fo:table-cell>
						<fo:block margin-left="0.5cm" font-size="14pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates mode="toc"/>						
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:when test="count(ancestor::node()) = 5">
					<fo:table-cell>
						<fo:block margin-left="1cm" font-size="12pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates mode="toc"/>						
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:when test="count(ancestor::node()) = 6">
					<fo:table-cell>
						<fo:block margin-left="1.5cm"  font-size="10pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates mode="toc"/>						
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:when test="count(ancestor::node()) = 7">
					<fo:table-cell>
						<fo:block margin-left="2cm"  font-size="8pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates mode="toc"/>						
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:otherwise>
					<fo:table-cell>
						<fo:block margin-left="2.5cm" font-size="6pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates mode="toc"/>						
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:otherwise>
			</xsl:choose>
		</fo:table-row>
	</xsl:template>
	<xsl:template match="archdesc/did/head" mode="toc">
		<fo:table-row>
			<fo:table-cell>
				<fo:block font-size="16pt">
					<fo:basic-link color="blue" internal-destination="{generate-id()}">
						<xsl:apply-templates mode="toc"/>						
					</fo:basic-link>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell text-align="right">
				<fo:block>
					<fo:page-number-citation ref-id="{generate-id()}"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
	</xsl:template>
	<xsl:template match="dsc/head" mode="toc">
		<fo:table-row>
			<fo:table-cell>
				<fo:block font-size="16pt">
					<fo:basic-link color="blue" internal-destination="{generate-id()}">
						<xsl:apply-templates mode="toc"/>						
					</fo:basic-link>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell text-align="right">
				<fo:block>
					<fo:page-number-citation ref-id="{generate-id()}"/>
				</fo:block>
			</fo:table-cell>
		</fo:table-row>
	</xsl:template>
	<xsl:template match="c01[@level='series'] | 
						       c02[@level='series'] | 
							c03[@level='series'] | 
							c04[@level='series'] | 
							c05[@level='series'] | 
							c06[@level='series'] | 
							c07[@level='series'] | 
							c08[@level='series'] | 
							c09[@level='series'] | 
							c10[@level='series'] | 
							c11[@level='series'] | 
							c12[@level='series'] | 
							c[@level='series'] |
	                                        c01[@level='subseries'] | 
						       c02[@level='subseries'] | 
							c03[@level='subseries'] | 
							c04[@level='subseries'] | 
							c05[@level='subseries'] | 
							c06[@level='subseries'] | 
							c07[@level='subseries'] | 
							c08[@level='subseries'] | 
							c09[@level='subseries'] | 
							c10[@level='subseries'] | 
							c11[@level='subseries'] | 
							c12[@level='subseries'] | 
							c[@level='subseries'] |
	                              c01[@level='subfonds'] | 
						       c02[@level='subfonds'] | 
							c03[@level='subfonds'] | 
							c04[@level='subfonds'] | 
							c05[@level='subfonds'] | 
							c06[@level='subfonds'] | 
							c07[@level='subfonds'] | 
							c08[@level='subfonds'] | 
							c09[@level='subfonds'] | 
							c10[@level='subfonds'] | 
							c11[@level='subfonds'] | 
							c12[@level='subfonds'] | 
							c[@level='subfonds']" mode="toc">
		<fo:table-row>
			<xsl:choose>
				<xsl:when test="count(ancestor::node()) = 4">
					<fo:table-cell>
						<fo:block margin-left="0.5cm" font-size="14pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates select="did/unitid"/>
								<xsl:text> </xsl:text>
								<xsl:apply-templates select="did/unittitle"/>
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:when test="count(ancestor::node()) = 5">
					<fo:table-cell>
						<fo:block margin-left="1cm" font-size="12pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates select="did/unitid"/>
								<xsl:text> </xsl:text>
								<xsl:apply-templates select="did/unittitle"/>
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:when test="count(ancestor::node()) = 6">
					<fo:table-cell>
						<fo:block margin-left="1.5cm" font-size="10pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates select="did/unitid"/>
								<xsl:text> </xsl:text>
								<xsl:apply-templates select="did/unittitle"/>
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:when test="count(ancestor::node()) = 7">
					<fo:table-cell>
						<fo:block margin-left="2cm" font-size="8pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates select="did/unitid"/>
								<xsl:text> </xsl:text>
								<xsl:apply-templates select="did/unittitle"/>
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:when test="count(ancestor::node()) = 8">
					<fo:table-cell>
						<fo:block margin-left="2.5cm" font-size="8pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates select="did/unitid"/>
								<xsl:text> </xsl:text>
								<xsl:apply-templates select="did/unittitle"/>
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:when>
				<xsl:otherwise>
					<fo:table-cell>
						<fo:block margin-left="3cm" font-size="8pt">
							<fo:basic-link color="blue" internal-destination="{generate-id()}">
								<xsl:apply-templates select="did/unitid"/>
								<xsl:text> </xsl:text>
								<xsl:apply-templates select="did/unittitle"/>
							</fo:basic-link>
						</fo:block>
					</fo:table-cell>
					<fo:table-cell text-align="right">
						<fo:block>
							<fo:page-number-citation ref-id="{generate-id()}"/>
						</fo:block>
					</fo:table-cell>
				</xsl:otherwise>
			</xsl:choose>
		</fo:table-row>
		<xsl:apply-templates mode="toc" select="c01[@level='series'] | 
						       c02[@level='series'] | 
							c03[@level='series'] | 
							c04[@level='series'] | 
							c05[@level='series'] | 
							c06[@level='series'] | 
							c07[@level='series'] | 
							c08[@level='series'] | 
							c09[@level='series'] | 
							c10[@level='series'] | 
							c11[@level='series'] | 
							c12[@level='series'] | 
							c[@level='series'] |
	                                        c01[@level='subseries'] | 
						       c02[@level='subseries'] | 
							c03[@level='subseries'] | 
							c04[@level='subseries'] | 
							c05[@level='subseries'] | 
							c06[@level='subseries'] | 
							c07[@level='subseries'] | 
							c08[@level='subseries'] | 
							c09[@level='subseries'] | 
							c10[@level='subseries'] | 
							c11[@level='subseries'] | 
							c12[@level='subseries'] | 
							c[@level='subseries'] |
	                              c01[@level='subfonds'] | 
						       c02[@level='subfonds'] | 
							c03[@level='subfonds'] | 
							c04[@level='subfonds'] | 
							c05[@level='subfonds'] | 
							c06[@level='subfonds'] | 
							c07[@level='subfonds'] | 
							c08[@level='subfonds'] | 
							c09[@level='subfonds'] | 
							c10[@level='subfonds'] | 
							c11[@level='subfonds'] | 
							c12[@level='subfonds'] | 
							c[@level='subfonds']"/>
	</xsl:template>
	
	<xsl:template match="note" mode="toc"></xsl:template>

	<!-- 


	
	*******************  PDF inhoudsopgave ************************ 
	
	-->
	<xsl:template match="head" mode="pdf-toc">
		<fox:outline internal-destination="{generate-id()}">
			<fox:label>
				<xsl:value-of select="."/>
			</fox:label>
			<xsl:apply-templates mode="pdf-toc" select="parent::*/*/head"/>
		</fox:outline>
	</xsl:template>
	<xsl:template match="archdesc/did/head" mode="pdf-toc">
		<fox:outline internal-destination="{generate-id()}">
			<fox:label>
				<xsl:value-of select="."/>
			</fox:label>
			<xsl:apply-templates mode="pdf-toc" select="
										/ead/archdesc/accessrestrict/head |
    										/ead/archdesc/accruals/head |
    										/ead/archdesc/acqinfo/head |
    										/ead/archdesc/altformavail/head |
    										/ead/archdesc/appraisal/head |
    										/ead/archdesc/arrangement/head |
    										/ead/archdesc/bibliography/head |
    										/ead/archdesc/bioghist/head |
    										/ead/archdesc/controlaccess/head |
    										/ead/archdesc/custodhist/head |
    										/ead/archdesc/descgrp/head |
    										/ead/archdesc/fileplan/head |
    										/ead/archdesc/index/head |
    										/ead/archdesc/odd/head |
    										/ead/archdesc/originalsloc/head |
    										/ead/archdesc/otherfindaid/head |
    										/ead/archdesc/phystech/head |
    										/ead/archdesc/prefercite/head |
    										/ead/archdesc/processinfo/head |
    										/ead/archdesc/relatedmaterial/head |
    										/ead/archdesc/scopecontent/head |
    										/ead/archdesc/separatedmaterial/head |
    										/ead/archdesc/userestrict/head"></xsl:apply-templates>
		</fox:outline>
	</xsl:template>
	<xsl:template match="dsc/head" mode="pdf-toc">
		<fox:outline internal-destination="{generate-id()}">
			<fox:label>
				<xsl:value-of select="."/>
			</fox:label>
			<xsl:apply-templates select="parent::*/c01 | parent::*/c" mode="pdf-toc"/>
		</fox:outline>
	</xsl:template>
	<xsl:template match="c01[@level='series'] | 
						       c02[@level='series'] | 
							c03[@level='series'] | 
							c04[@level='series'] | 
							c05[@level='series'] | 
							c06[@level='series'] | 
							c07[@level='series'] | 
							c08[@level='series'] | 
							c09[@level='series'] | 
							c10[@level='series'] | 
							c11[@level='series'] | 
							c12[@level='series'] | 
							c[@level='series'] |
	                                        c01[@level='subseries'] | 
						       c02[@level='subseries'] | 
							c03[@level='subseries'] | 
							c04[@level='subseries'] | 
							c05[@level='subseries'] | 
							c06[@level='subseries'] | 
							c07[@level='subseries'] | 
							c08[@level='subseries'] | 
							c09[@level='subseries'] | 
							c10[@level='subseries'] | 
							c11[@level='subseries'] | 
							c12[@level='subseries'] | 
							c[@level='subseries'] |
	                              c01[@level='subfonds'] | 
						       c02[@level='subfonds'] | 
							c03[@level='subfonds'] | 
							c04[@level='subfonds'] | 
							c05[@level='subfonds'] | 
							c06[@level='subfonds'] | 
							c07[@level='subfonds'] | 
							c08[@level='subfonds'] | 
							c09[@level='subfonds'] | 
							c10[@level='subfonds'] | 
							c11[@level='subfonds'] | 
							c12[@level='subfonds'] | 
							c[@level='subfonds']" mode="pdf-toc">
		<xsl:choose>
			<xsl:when test="count(ancestor::node()) = 4">
				<fox:outline internal-destination="{generate-id()}">
					<fox:label>
						<xsl:value-of select="did/unitid"/>
						<xsl:text> </xsl:text>
						<xsl:value-of select="did/unittitle"/>
					</fox:label>
					<xsl:apply-templates mode="pdf-toc" select="c01[@level='series'] | 
												       c02[@level='series'] | 
													c03[@level='series'] | 
													c04[@level='series'] | 
													c05[@level='series'] | 
													c06[@level='series'] | 
													c07[@level='series'] | 
													c08[@level='series'] | 
													c09[@level='series'] | 
													c10[@level='series'] | 
													c11[@level='series'] | 
													c12[@level='series'] | 
													c[@level='series'] |
							                                        c01[@level='subseries'] | 
												       c02[@level='subseries'] | 
													c03[@level='subseries'] | 
													c04[@level='subseries'] | 
													c05[@level='subseries'] | 
													c06[@level='subseries'] | 
													c07[@level='subseries'] | 
													c08[@level='subseries'] | 
													c09[@level='subseries'] | 
													c10[@level='subseries'] | 
													c11[@level='subseries'] | 
													c12[@level='subseries'] | 
													c[@level='subseries'] |
							                              c01[@level='subfonds'] | 
												       c02[@level='subfonds'] | 
													c03[@level='subfonds'] | 
													c04[@level='subfonds'] | 
													c05[@level='subfonds'] | 
													c06[@level='subfonds'] | 
													c07[@level='subfonds'] | 
													c08[@level='subfonds'] | 
													c09[@level='subfonds'] | 
													c10[@level='subfonds'] | 
													c11[@level='subfonds'] | 
													c12[@level='subfonds'] | 
													c[@level='subfonds']"/>
				</fox:outline>
			</xsl:when>
			<xsl:when test="count(ancestor::node()) = 5">
				<fox:outline internal-destination="{generate-id()}">
					<fox:label>
						<xsl:value-of select="did/unitid"/>
						<xsl:text> </xsl:text>
						<xsl:value-of select="did/unittitle"/>
					</fox:label>
					<xsl:apply-templates mode="pdf-toc" select="c01[@level='series'] | 
												       c02[@level='series'] | 
													c03[@level='series'] | 
													c04[@level='series'] | 
													c05[@level='series'] | 
													c06[@level='series'] | 
													c07[@level='series'] | 
													c08[@level='series'] | 
													c09[@level='series'] | 
													c10[@level='series'] | 
													c11[@level='series'] | 
													c12[@level='series'] | 
													c[@level='series'] |
							                                        c01[@level='subseries'] | 
												       c02[@level='subseries'] | 
													c03[@level='subseries'] | 
													c04[@level='subseries'] | 
													c05[@level='subseries'] | 
													c06[@level='subseries'] | 
													c07[@level='subseries'] | 
													c08[@level='subseries'] | 
													c09[@level='subseries'] | 
													c10[@level='subseries'] | 
													c11[@level='subseries'] | 
													c12[@level='subseries'] | 
													c[@level='subseries'] |
							                              c01[@level='subfonds'] | 
												       c02[@level='subfonds'] | 
													c03[@level='subfonds'] | 
													c04[@level='subfonds'] | 
													c05[@level='subfonds'] | 
													c06[@level='subfonds'] | 
													c07[@level='subfonds'] | 
													c08[@level='subfonds'] | 
													c09[@level='subfonds'] | 
													c10[@level='subfonds'] | 
													c11[@level='subfonds'] | 
													c12[@level='subfonds'] | 
													c[@level='subfonds']"/>
				</fox:outline>
			</xsl:when>
			<xsl:when test="count(ancestor::node()) = 6">
				<fox:outline internal-destination="{generate-id()}">
					<fox:label>
						<xsl:value-of select="did/unitid"/>
						<xsl:text> </xsl:text>
						<xsl:value-of select="did/unittitle"/>
					</fox:label>
					<xsl:apply-templates mode="pdf-toc" select="c01[@level='series'] | 
												       c02[@level='series'] | 
													c03[@level='series'] | 
													c04[@level='series'] | 
													c05[@level='series'] | 
													c06[@level='series'] | 
													c07[@level='series'] | 
													c08[@level='series'] | 
													c09[@level='series'] | 
													c10[@level='series'] | 
													c11[@level='series'] | 
													c12[@level='series'] | 
													c[@level='series'] |
							                                        c01[@level='subseries'] | 
												       c02[@level='subseries'] | 
													c03[@level='subseries'] | 
													c04[@level='subseries'] | 
													c05[@level='subseries'] | 
													c06[@level='subseries'] | 
													c07[@level='subseries'] | 
													c08[@level='subseries'] | 
													c09[@level='subseries'] | 
													c10[@level='subseries'] | 
													c11[@level='subseries'] | 
													c12[@level='subseries'] | 
													c[@level='subseries'] |
							                              c01[@level='subfonds'] | 
												       c02[@level='subfonds'] | 
													c03[@level='subfonds'] | 
													c04[@level='subfonds'] | 
													c05[@level='subfonds'] | 
													c06[@level='subfonds'] | 
													c07[@level='subfonds'] | 
													c08[@level='subfonds'] | 
													c09[@level='subfonds'] | 
													c10[@level='subfonds'] | 
													c11[@level='subfonds'] | 
													c12[@level='subfonds'] | 
													c[@level='subfonds']"/>
				</fox:outline>
			</xsl:when>
			<xsl:otherwise>
				<fox:outline internal-destination="{generate-id()}">
					<fox:label>
						<xsl:value-of select="did/unitid"/>
						<xsl:text> </xsl:text>
						<xsl:value-of select="did/unittitle"/>
					</fox:label>
					<xsl:apply-templates mode="pdf-toc" select="c01[@level='series'] | 
												       c02[@level='series'] | 
													c03[@level='series'] | 
													c04[@level='series'] | 
													c05[@level='series'] | 
													c06[@level='series'] | 
													c07[@level='series'] | 
													c08[@level='series'] | 
													c09[@level='series'] | 
													c10[@level='series'] | 
													c11[@level='series'] | 
													c12[@level='series'] | 
													c[@level='series'] |
							                                        c01[@level='subseries'] | 
												       c02[@level='subseries'] | 
													c03[@level='subseries'] | 
													c04[@level='subseries'] | 
													c05[@level='subseries'] | 
													c06[@level='subseries'] | 
													c07[@level='subseries'] | 
													c08[@level='subseries'] | 
													c09[@level='subseries'] | 
													c10[@level='subseries'] | 
													c11[@level='subseries'] | 
													c12[@level='subseries'] | 
													c[@level='subseries'] |
							                              c01[@level='subfonds'] | 
												       c02[@level='subfonds'] | 
													c03[@level='subfonds'] | 
													c04[@level='subfonds'] | 
													c05[@level='subfonds'] | 
													c06[@level='subfonds'] | 
													c07[@level='subfonds'] | 
													c08[@level='subfonds'] | 
													c09[@level='subfonds'] | 
													c10[@level='subfonds'] | 
													c11[@level='subfonds'] | 
													c12[@level='subfonds'] | 
													c[@level='subfonds']"/>
				</fox:outline>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<!--


	******************************* @audience afvangen ****************

	
-->
	<xsl:template match="text()">
		<xsl:choose>
			<xsl:when test="ancestor::*[@audience='internal'] and $in_or_external='external'"></xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."></xsl:value-of>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template match="did//persname">
		<xsl:choose>
			<xsl:when test="$in_or_external='external'">
				<xsl:choose>
					<xsl:when 
					test="number(substring(ancestor::did/unitdate/@normal, string-length(ancestor::did/unitdate/@normal) - 3)) > $year">
						<xsl:text>***</xsl:text>		
					</xsl:when>
					<xsl:otherwise>
						<xsl:apply-templates/>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	
	
</xsl:stylesheet>
