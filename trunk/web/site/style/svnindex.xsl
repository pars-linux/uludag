<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- gezinme menusu -->
<xsl:template name="navmenu" >
	<a href="/" >Ana Sayfa</a>
	<a href="/hakkimizda/" >Hakkımızda</a>
	<div class="submenu" >
		<a><xsl:attribute  name="href" ><![CDATA[/hakkimizda/tarihce.xml]]></xsl:attribute>Tarihçe</a>
		<a><xsl:attribute  name="href" ><![CDATA[/hakkimizda/kimiz.xml]]></xsl:attribute>Biz Kimiz?</a>
	</div>
	<a href="/projeler/" >Projeler</a>
	<div class="submenu" >
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/paketler/]]></xsl:attribute>Paketler</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/pisi/]]></xsl:attribute>Paket Yönetim Sistemi</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/comar/]]></xsl:attribute>Yapılandırma Araçları</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/yali/]]></xsl:attribute>Kurulum</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/turkce/]]></xsl:attribute>Türkçe</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/belgeler/]]></xsl:attribute>Belgeler</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/grafik/]]></xsl:attribute>Grafik &amp; Medya</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/ibe/]]></xsl:attribute>İBE</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/kalite/]]></xsl:attribute>Kalite Güvence</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/iliskiler/]]></xsl:attribute>Katkıcı İlişkileri</a>
		<a><xsl:attribute  name="href" ><![CDATA[/projeler/gelistirici/]]></xsl:attribute>Geliştirici Sistemi</a>
	</div>
	<a href="/sss/" >Sıkça Sorulanlar</a>
	<a href="/servisler.xml" >Servisler</a>
	<a href="/en/" >English</a>
</xsl:template>

  
<xsl:output method="html"/>

<xsl:template match="*"/>

<xsl:template match="svn">
    <html>
      <head>
        <title>
          <xsl:if test="string-length(index/@name) != 0">
            <xsl:value-of select="index/@name"/>
            <xsl:text>: </xsl:text>
          </xsl:if>
          <xsl:value-of select="index/@path"/>
        </title>
        <link rel="stylesheet" type="text/css" href="/style/svnindex.css"/>
	<link rel="shortcut icon" type="image/x-icon" href="/img/favicon.ico"/>
      </head>
      <body>

      <table class="header" cellspacing="0" >
	<tr>
	  <td class="headerleft" >
	    <a href="/" ><img src="/img/logo.png" /></a>
	  </td>
	  <td class="header" >
	   <a href="/" >Uludağ</a>
	  </td>
	</tr>
	<tr>
	  <td class="headerdesc" colspan="2" >
	     Linux temelli ulusal işletim sistemi
	  </td>
	</tr>
      </table>

      <table class="content" cellspacing="0" >
      <tr>
      <td class="leftmenu" >
      <div class="leftbox" >
      <xsl:call-template xmlns:xsl="http://www.w3.org/1999/XSL/Transform" name="navmenu" />
      </div>
      <div class="leftbox" >
      <form target="_blank" method="get" action="http://www.google.com/search" >
      <input type="hidden" value="www.uludag.org.tr" name="sitesearch" />
      <input size="15" onblur="if(this.value=='') this.value='Arama...';" value="Arama..." type="text" onfocus="if(this.value=='Arama...') this.value='';" id="query" name="q" />
      </form>
      </div>
      </td>
      <td class="content" >

  <div id="svn">
          <xsl:apply-templates/>
        </div>
        <div id="footer">
          <xsl:text>Powered by </xsl:text>
          <xsl:element name="a">
            <xsl:attribute name="href">
              <xsl:value-of select="@href"/>
            </xsl:attribute>
            <xsl:text>Subversion</xsl:text>
          </xsl:element>
          <xsl:text> </xsl:text>
          <xsl:value-of select="@version"/>
        </div>

      <div class="content" >
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


<xsl:template match="index">
    <div id="rev">
      <xsl:if test="string-length(@name) != 0">
        <xsl:value-of select="@name"/>
        <xsl:if test="string-length(@rev) != 0">
          <xsl:text> &#8212; </xsl:text>
        </xsl:if>
      </xsl:if>
      <xsl:if test="string-length(@rev) != 0">
        <xsl:text>Revision </xsl:text>
        <xsl:value-of select="@rev"/>
      </xsl:if>
    </div>
    <div id="path">
      <xsl:value-of select="@path"/>
    </div>
    <xsl:apply-templates select="updir"/>
    <xsl:apply-templates select="dir"/>
    <xsl:apply-templates select="file"/>
  </xsl:template>

  <xsl:template match="updir">
    <div id="updir">
      <xsl:text>[</xsl:text>
      <xsl:element name="a">
        <xsl:attribute name="href">..</xsl:attribute>
        <xsl:text>Parent Directory</xsl:text>
      </xsl:element>
      <xsl:text>]</xsl:text>
    </div>
    <!-- xsl:apply-templates/ -->
  </xsl:template>

  <xsl:template match="dir">
    <div id="dir">
      <xsl:element name="a">
        <xsl:attribute name="href">
          <xsl:value-of select="@href"/>
        </xsl:attribute>
        <xsl:value-of select="@name"/>
        <xsl:text>/</xsl:text>
      </xsl:element>
    </div>
    <!-- <xsl:apply-templates/ -->
  </xsl:template>

  <xsl:template match="file">
    <div id="file">
      <xsl:element name="a">
        <xsl:attribute name="href">
          <xsl:value-of select="@href"/>
        </xsl:attribute>
        <xsl:value-of select="@name"/>
      </xsl:element>
    </div>
    <!-- xsl:apply-templates/ -->
</xsl:template>

</xsl:stylesheet>
