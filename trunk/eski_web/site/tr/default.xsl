<?xml version = '1.0' encoding = 'utf-8'?>
<!-- 
  Hazırlanan Ulusal Dağıtım XML dosyalarının HTML formatına çevrimi için
  kullanılır.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" encoding="utf-8" >

<xsl:output
       method="xml"
       omit-xml-declaration="no"
       indent="no"
       encoding="utf-8"
       doctype-public='"-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"'
       />

<xsl:include href="../genel.xsl" />

<!-- gezinme menusu -->
<xsl:template name="navmenu" >
	<a href="/" >Ana Sayfa</a>
	<a href="/hakkimizda/" >Hakkımızda</a>
	<div class="submenu" >
		<a><xsl:attribute name="href"><![CDATA[/hakkimizda/tarihce.xml]]></xsl:attribute>Tarihçe</a>
		<a><xsl:attribute name="href"><![CDATA[/hakkimizda/kimiz.xml]]></xsl:attribute>Biz Kimiz?</a>
	</div>
	<a href="/projeler/" >Projeler</a>
	<div class="submenu" >
		<a><xsl:attribute name="href"><![CDATA[/projeler/paketler/]]></xsl:attribute>Paketler</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/pisi/]]></xsl:attribute>Paket Yönetim Sistemi</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/comar/]]></xsl:attribute>Yapılandırma Araçları</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/yali/]]></xsl:attribute>Kurulum</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/turkce/]]></xsl:attribute>Türkçe</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/grafik/]]></xsl:attribute>Grafik &amp; Medya</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/ibe/]]></xsl:attribute>İBE</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/kalite/]]></xsl:attribute>Kalite Güvence</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/iliskiler/]]></xsl:attribute>Katkıcı İlişkileri</a>
		<a><xsl:attribute name="href"><![CDATA[/projeler/gelistirici/]]></xsl:attribute>Geliştirici Sistemi</a>
	</div>
	<a href="/sss/">Sıkça Sorulanlar</a>
	<a href="/servisler.xml">Servisler</a>
	<a href="/en/">English</a>
</xsl:template>

<xsl:template name="header" >
	<table class="header" cellspacing="0" >
	<tr>
		<td class="headerleft" >
			<a href="/" ><img src="/img/logo.png" /></a>
		</td>
		<td class="header" >
			<a href="/" >Ulusal Dağıtım</a>
		</td>
	</tr>
	<tr>
		<td class="headerdesc" colspan="2" >
			Linux temelli ulusal işletim sistemi
		</td>
	</tr>
	</table>
</xsl:template>

<xsl:template match="book" >

	<html xmlns="http://www.w3.org/TR/xhtml1/strict">
	<head>
		<link rel="stylesheet" href="/style/webstyles.css" type="text/css" />
		<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
		<link rel="shortcut icon" type="image/x-icon" href="/img/favicon.ico" />
		<title>
			<xsl:value-of select="//book/bookinfo/title" />
		</title>
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
					<input type="hidden" value="www.uludag.org.tr" name="sitesearch" />
					<input size="15" onblur="if(this.value=='') this.value='Arama...';" value="Arama..." type="text" onfocus="if(this.value=='Arama...') this.value='';" id="query" name="q" />
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
			Ulusal Dağıtım <em>copyleft</em> 2004<br/>
		</div>
	</body>
	</html>
</xsl:template>

</xsl:stylesheet>
