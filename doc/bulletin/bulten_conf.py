#!/usr/bin/env python
# -*- coding: utf-8 -*-

SITENAME = "Uludağ Weekly Newsletter"
LOGS = "bultenler"
ARCHIVE = "arsiv"

entry_count = 0 # entries printed in first page

index_file = LOGS + "/.index"
log_prefix = ".txt"

header_text = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
	<title>:: ulusal dağıtım project :: tübitak-uekae ::</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<link href="../../../stil.css" rel="stylesheet" type="text/css">
	<link rel="shortcut icon" type="image/x-icon" href="../../../images/favicon.ico">
</head>

<body class="arka">
<table class="arkayan" width="800" border="0" align="center" cellpadding="0" cellspacing="0">
<tr>
<td width="878" align="center" valign="top">
<table class="arkadalga" width="700" align="center" cellpadding="0" cellspacing="0">
<tr>
<td width="800" valign="top">

<!-- logo -->
<table width="700" border="0" align="center" cellpadding="0" cellspacing="0">
<tr>
<td width="620" height="60">
<img src="../../../images/header3.png" alt="Ulusal Dağıtım Projesi" width="700" height="60">
</td>
</tr>

<!-- menüler -->
<tr>
<td width="680" height="19" valign="top" bgcolor="#B9D0B3">
<p class="menubar">
<a href="../../index.html">Home</a>
| <a href="../../hakkimizda.html">About</a>
| <a href="../../projeler/index.html">Projects</a>
| <a href="../../belgeler/index.html">Documents</a>
| <a href="../../urunler/index.html">Products</a>
| <a href="../../sss.html">FAQ</a>
| <a href="../../iletisim.html">Contact Us</a>
| <a href="../../basin/index.html">Press</a>
| <a href="../../../index.html">Türkçe</a>
</p>
</tr>
</table>

<br>

<!-- SAYFA İÇERİK BAŞI -->

<table width="695" border="0" cellspacing="0" cellpadding="0">
<tr>
<td width="20" valign="top"><img src="../images/bullet6.png" width="20" height="20" hspace="0" vspace="0" align="top"></td>
<td width="10" valign="top">&nbsp;</td>
               <td width="661" valign="top" class="metin"><p><span class="baslik"><font face="Verdana, Arial, Helvetica, sans-serif">Ulusal Dağıtım Newsletters</font></span><br><br><br>

'''

archive_header = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
	<title>:: ulusal dağıtım project :: tübitak-uekae ::</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<link href="../../stil.css" rel="stylesheet" type="text/css">
	<link rel="shortcut icon" type="image/x-icon" href="../../images/favicon.ico">
</head>

<body class="arka">
<table class="arkayan" width="800" border="0" align="center" cellpadding="0" cellspacing="0">
<tr>
<td width="878" align="center" valign="top">
<table class="arkadalga" width="700" align="center" cellpadding="0" cellspacing="0">
<tr>
<td width="800" valign="top">

<!-- logo -->
<table width="700" border="0" align="center" cellpadding="0" cellspacing="0">
<tr>
<td width="620" height="60">
<img src="../../images/header3.png" alt="Ulusal Dağıtım Projesi" width="700" height="60">
</td>
</tr>

<!-- menüler -->
<tr>
<td width="680" height="19" valign="top" bgcolor="#B9D0B3">
<p class="menubar">
<a href="../index.html">Home</a>
| <a href="../hakkimizda.html">About</a>
| <a href="../projeler/index.html">Projects</a>
| <a href="../belgeler/index.html">Documents</a>
| <a href="../urunler/index.html">Products</a>
| <a href="../sss.html">FAQ</a>
| <a href="../iletisim.html">Contact Us</a>
| <a href="../basin/index.html">Press</a>
| <a href="../../index.html">Türkçe</a>
</p>
</tr>
</table>

<br>

<!-- SAYFA İÇERİK BAŞI -->

<table width="695" border="0" cellspacing="0" cellpadding="0">
<tr>
<td width="20" valign="top"><img src="../../images/bullet6.png" width="20" height="20" hspace="0" vspace="0" align="top"></td>
<td width="10" valign="top">&nbsp;</td>
               <td width="661" valign="top" class="metin"><p><span class="baslik"><font face="Verdana, Arial, Helvetica, sans-serif">Newsletter Archive</font></span><br><br><br>
'''

footer_text = '''
</table>

<!-- SAYFA İÇERİK SONU -->

<!-- yayın hakkı -->
<br>
<br>
<p class="not">
Information and documents on Uludağ Project web pages can be used freely anywhere with original source credit.
<em><br>
<strong>TÜBİTAK - UEKAE, PK.74 41470, Gebze / Kocaeli.</strong></em>
For information and suggestion(s) please write to <a href="mailto:bilgi%20at%20uludag.org.tr">bilgi
at uludag.org.tr</a>
</p>
<br>

</td>
</tr>
</table>

</td>
</tr>
</table>

</body>
</html>
'''
