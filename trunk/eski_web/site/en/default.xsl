<?xml version = '1.0' encoding = 'utf-8'?>
<!--
  Hazırlanan Uludağ XML dosyalarının HTML formatına çevrimi için
  kullanılır.
-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" encoding="utf-8" >
<xsl:output 
	method="xml"
	omit-xml-declaration="no"
	indent="no"
	encoding="utf-8"
	/>

<xsl:include href="../genel.xsl" />

<!-- gezinme menusu -->
<xsl:template xmlns:xsl="http://www.w3.org/1999/XSL/Transform" name="navmenu" >
	<a href="/en" >Home Page</a>
	<a href="/en/aboutus/" >About Us</a>
		<div class="submenu" >
		<a><xsl:attribute name="href"><![CDATA[/en/aboutus/history.xml]]></xsl:attribute>History</a>
		<a><xsl:attribute name="href"><![CDATA[/en/aboutus/whower.xml]]></xsl:attribute>Who We Are</a>
		</div>
	<a href="/en/projects/" >Projects</a>
		<div class="submenu" >
		<a><xsl:attribute name="href"><![CDATA[/en/projects/packages/]]></xsl:attribute>Packages</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/pisi/]]></xsl:attribute>Packege Management System</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/comar/]]></xsl:attribute>Configuration Tools</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/yali/]]></xsl:attribute>Installer</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/turkish/]]></xsl:attribute>Turkish</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/graphics/]]></xsl:attribute>Graphics &amp; Media</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/hci/]]></xsl:attribute>HCI</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/quality/]]></xsl:attribute>Quality Assurance</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/relations/]]></xsl:attribute>Contributor Relations</a>
		<a><xsl:attribute name="href"><![CDATA[/en/projects/developer/]]></xsl:attribute>Developer System</a>
		</div>
	<a href="/en/faq/" >FAQ</a>
	<a href="/" >Türkçe</a>
</xsl:template>

<xsl:template name="header">
	<table class="header" cellspacing="0" >
	<tr>
		<td class="headerleft" >
			<a href="/" >
			<img src="/img/logo.png" alt="LOGO"/>
			</a>
		</td>
		<td class="header" >
			<a href="/en" >Uludağ</a>
		</td>
	</tr>
	<tr>
		<td class="headerdesc" colspan="2" >
			Linux based Turkish OS distribution
	        </td>
	</tr>
	</table>
</xsl:template>

<xsl:template match="book" >

<html xmlns="http://www.w3.org/TR/xhtml1/strict">
<head>
	<link rel="stylesheet" type="text/css" href="/style/webstyles.css" />
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<link rel="shortcut icon" href="/img/favicon.ico" type="image/x-icon" />
	<title><xsl:value-of select="//book/bookinfo/title" /></title>
</head>

<body>
	<xsl:call-template name="header" />
	<table class="content" cellspacing="0" >
	<tr>
		<td class="leftmenu" >
		<div class="leftbox" >
			<xsl:call-template name="navmenu" />
		</div>
		<div class="leftbox" >
			<form target="_blank" method="get" action="http://www.google.com/search" >
			<input value="www.uludag.org.tr" type="hidden" name="sitesearch" />
			<input size="15" onblur="if(this.value=='') this.value='Search...';" type="text" value="Search..." id="query" onfocus="if(this.value=='Search...') this.value='';" name="q" />
			</form>
		</div>
		</td>
		
		<td class="content" >
		<div class="content" >
			<xsl:apply-templates />
		</div>
		</td>
	</tr>
	</table>
	
	<div class="pagefooter" >
         Uludağ <em>copyleft</em> 2004<br/>
	</div>
</body>
</html>
</xsl:template>

</xsl:stylesheet>
