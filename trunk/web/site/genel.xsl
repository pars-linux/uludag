<?xml version="1.0" encoding="utf-8"?>

<!--
  Hemen hemen tüm xsl'ler tarafından kullanılan gelen bir menü.
  Bu menü içerisinde HTML'e dünüştürülecek alt bileşenlerin tarifleri
  yapılıyor.
-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:template match="bookinfo" name="bookinfo">
<div class="bookinfo">
  <span class="title"><xsl:value-of select="title/text()"/></span>
  <!-- book[@type='guide'] ise bookinfo'yu yazdir... -->
  <xsl:if test="/book[attribute::type='guide']">
    <xsl:for-each select="author">
      <div class="author">
        <xsl:value-of select="firstname"/>
        <xsl:value-of select="lastname"/>
        <xsl:for-each select="address/email">
          <a class="email">
            <xsl:attribute name="href">mailto:<xsl:value-of select="text()"/></xsl:attribute>
            <xsl:value-of select="text()"/>
          </a>
        </xsl:for-each> <!-- address/email -->
	<xsl:for-each select="address/web">
	  <a class="authorweb">
            <xsl:attribute name="href">
              <xsl:value-of select="text()"/>
            </xsl:attribute>
            <xsl:value-of select="text()"/>
          </a>
	</xsl:for-each> <!-- address/web -->
      </div>
    </xsl:for-each> <!-- bookinfo/author -->
    <span class="pubdate">Son güncellenme tarihi: <xsl:value-of select="pubdate/text()"/></span>
  </xsl:if> <!-- book[@type='guide'] -->

  <xsl:for-each select="abstract/para">
    <div class="abstract">
      <xsl:value-of select="text()"/>
    </div>
  </xsl:for-each>
    
</div>
</xsl:template>

<xsl:template match="//para">
<p><xsl:apply-templates/></p>
</xsl:template>

<!-- email'i link olarak göster -->
<xsl:template match="//email">
<a class="email">
  <xsl:attribute name="href">
    mailto:<xsl:value-of select="text()"/>
  </xsl:attribute>
  <xsl:value-of select="text()"/>
</a>
</xsl:template>

<xsl:template match="//graphic">
  <img>
       <xsl:attribute name="src">
         <xsl:value-of select="@source"/>
       </xsl:attribute>
       <xsl:if test="@align">
         <xsl:attribute name="align">
	   <xsl:value-of select="@align"/>
	 </xsl:attribute>
       </xsl:if>
  </img>
</xsl:template>

<xsl:template match="//link">
  <a>
       <xsl:attribute name="href">
         <xsl:if test="@thispage"> <!-- sayfa içerisinde yerel link -->
           #<xsl:value-of select="@thispage"/>
	 </xsl:if>
	 <xsl:if test="@url">
           <xsl:value-of select="@url"/>
         </xsl:if>
       </xsl:attribute>
       <xsl:value-of select="text()"/>
  </a>
</xsl:template> 

<xsl:template match="orderedlist">
<div class="orderedlist"><xsl:apply-templates/></div>
</xsl:template>

<!-- şimdilik numberedlist == orderedlist, daha sonra burada sayılar ile göstereceğiz -->
<xsl:template match="numberedlist">
<div class="numberedlist"><xsl:apply-templates/></div>
</xsl:template>

<!-- şimdilik descriptivelist == orderedlist, daha sonra burada sayılar ile göstereceğiz -->
<xsl:template match="descriptivelist">
<div class="descriptivelist"><xsl:apply-templates/></div>
</xsl:template>

<xsl:template match="*/listitem">
<span class="listitem"><xsl:apply-templates/></span>
</xsl:template>

<xsl:template match="//note">
<div class="note">
  <u>NOT:</u> <xsl:value-of select="text()"/>
</div>
</xsl:template>

<xsl:template match="//attention">
<div class="attention">
  <u>DİKKAT:</u> <xsl:value-of select="text()"/>
</div>
</xsl:template>

<xsl:template match="//footer">
<div class="footer">
  <xsl:apply-templates/>
</div>
</xsl:template>


<!-- 
     chapter 
     tüm chapter tek bir div'de
-->
<xsl:template match="chapter">
<div class="chapter">
  <xsl:apply-templates/>
</div>
</xsl:template>
 
<xsl:template match="chapter/chapterinfo/abstract">
  <div class="abstract">
    <xsl:apply-templates/>
  </div>
</xsl:template>


<!-- chapter/title bir anchor olarak gözüksün  -->
<xsl:template match="chapter/chapterinfo/title" name="titlelink">
  <span class="title">
    <a>
      <xsl:attribute name="name"><xsl:value-of select="text()"/></xsl:attribute>
      <xsl:value-of select="text()"/>
    </a>
  </span>
</xsl:template>

<xsl:template match="//sect1">
  <div class="sect1">
    <xsl:apply-templates/>
  </div>
</xsl:template>
<xsl:template match="//sect1/title">
  <xsl:call-template name="titlelink"/>
</xsl:template>

<xsl:template match="//sect2">
  <div class="sect2">
    <xsl:apply-templates/>
  </div>
</xsl:template>
<xsl:template match="//sect2/title">
  <xsl:call-template name="titlelink"/>
</xsl:template>

<xsl:template match="//sect3">
  <div class="sect3">
    <xsl:apply-templates/>
  </div>
</xsl:template>
<xsl:template match="//sect3/title">
  <xsl:call-template name="titlelink"/>
</xsl:template>


<xsl:template match="//program">
<div class="program">
  <pre>
  <xsl:apply-templates/>
  </pre>
</div>
</xsl:template>

<xsl:template match="//command">
<div class="command">
  <pre>
  <xsl:apply-templates/>
  </pre>
</div>
</xsl:template>

<xsl:template match="//em">
<em><xsl:apply-templates/></em>
</xsl:template>
<xsl:template match="//underline">
<u><xsl:apply-templates/></u>
</xsl:template>
<xsl:template match="//strong">
<strong><xsl:apply-templates/></strong>
</xsl:template>

</xsl:stylesheet>

