<?xml version="1.0"?>

<!--
  XML dosyalarından 'yazıcı dostu' HTML sayfaları üretir.
-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:include href="genel.xsl"/>

<xsl:template match="book">
<html>
 <head>
   <link type="text/css" rel="stylesheet" href="/style/webstyles.css"/>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
 </head>
 <body>

	       <xsl:apply-templates/>
  
 </body>
</html>
</xsl:template>

</xsl:stylesheet>
