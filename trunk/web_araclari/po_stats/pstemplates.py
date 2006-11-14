#-*- coding: utf-8 -*-

#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

"""

   There must be three template variable for every language. Here is an example for "en":

------>8-------------->8------------->8------------>8------------>8------------>8------------------

htmlHeaderTemplate["en"] = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
                            <html><body>'''

htmlBodyTemplate["en"] = '''<table border="1" align="center" width="90%%" cellspacing="1" cellpadding="5">
                            <tr><td colspan="6">%(Language-Team)s (<b>%(Project-Id-Version)s</b>)</td></tr>
                            <tr><td>File</td><td>Total Messages</td><td>Translated</td><td>Fuzzy</td><td>Untranslated</td></tr>
                            <tr><td>%(File-Name)s</td><td>%(Total)s</td><td>%(Translated)s</td><td>%(Fuzzy)s</td><td>%(Untranslated)s</td></tr>
                            </table>'''

htmlFooterTemplate["en"] = '''</html></body>'''

------8<--------------8<-------------8<------------8<------------8<------------8<------------------
"""

htmlHeaderTemplate = {}
htmlBodyTemplate = {}
htmlFooterTemplate = {}



## en

htmlHeaderTemplate["en"] = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
        <title>:: ulusal dağıtım project :: tübitak-uekae ::</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link href="../../../../stil.css" rel="stylesheet" type="text/css">
        <link rel="shortcut icon" type="image/x-icon" href="../../../../images/favicon.ico">

        <style type="text/css">
            .tdh {
                text-align: center;
                font-weight: bold;
                background-color: #DDD;
                border-bottom: 1px #000 solid;
            }

            .itd {
                border-bottom: 1px #DDD dashed;
                text-align: center;
            }

            .fitd {
                border-bottom: 1px #DDD dashed;
            }

        </style>
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
<img src="../../../../images/header3.png" alt="Pardus Linux" width="700" height="60">
</td>
</tr>

<!-- menüler -->
<tr>
<td width="680" height="19" valign="top" bgcolor="#B9D0B3">
<p class="menubar">
<a href="../../../index.html">Home</a>
| <a href="../../../info.html">About</a>
| <a href="../../../projects/index.html">Projects</a>
| <a href="../../../documents/index.html">Documents</a>
| <a href="../../../products/index.html">Products</a>
| <a href="../../../contact.html">Contact Us</a>
| <a href="../../../press/index.html">Press</a>
| <a href="../../../../index.html">Türkçe</a>
</p>
</tr>
</table>

<br>

<p><img src="../../../images/bullet6.png" alt="nokta" align="top"><span class="baslik"> Stats for -<b>%s</b>-</span>

<p><center><table style="width: 90%%;">
<tr>
    <td class="tdh">File</td>
    <td class="tdh">Total Messages</td>
    <td class="tdh">Translated</td>
    <td class="tdh">Fuzzy</td>
    <td class="tdh">Untranslated</td>
</tr>
'''

htmlBodyTemplate["en"] = '''
<tr>
    <td class="fitd"><a href="%(File-Path)s">%(Project-Id-Version)s</a></td>
    <td class="itd">%(Total)s</td>
    <td class="itd">%(Translated)s</td>
    <td class="itd">%(Fuzzy)s</td>
    <td class="itd">%(Untranslated)s</td>
</tr>'''

htmlFooterTemplate["en"] = '''
</table></center>
<br>
<br>
<p class="not">
Information and documents on Pardus web pages can be used freely anywhere with original source credit.
<em><br>
<strong>TÜBİTAK - UEKAE, PK.74 41470, Gebze / Kocaeli.</strong></em>
For information and suggestion(s) please write to <a href="mailto:bilgi%20at%20pardus.org.tr">bilgi at pardus.org.tr</a>
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




## tr

htmlHeaderTemplate["tr"] = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
   <title>:: Pardus :: tübitak-uekae ::</title>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <link href="../../../stil.css" rel="stylesheet" type="text/css">
   <link rel="shortcut icon" type="image/x-icon" href="../../../images/favicon.ico">


        <style type="text/css">
            .tdh {
                text-align: center;
                font-weight: bold;
                background-color: #DDD;
                border-bottom: 1px #000 solid;
            }

            .itd {
                border-bottom: 1px #DDD dashed;
                text-align: center;
            }

            .fitd {
                border-bottom: 1px #DDD dashed;
            }

        </style>

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
<img src="../../../images/header3.png" alt="Pardus" width="700" height="60">
</td>
</tr>

<!-- menüler -->
<tr>
<td width="680" height="19" valign="top" bgcolor="#B9D0B3">
<p class="menubar">
<a href="../../../index.html">Ana Sayfa</a>
| <a href="../../../hakkimizda.html">Hakkımızda</a>
| <a href="../../../projeler/index.html">Projeler</a>
| <a href="../../../belgeler/index.html">Belgeler</a>
| <a href="../../../urunler/index.html">Ürünler</a>
| <a href="../../../iletisim.html">İletişim</a>
| <a href="../../../basin/index.html">Basında Pardus</a>
| <a href="../../../eng/index.html">English</a>
</p>
</tr>
</table>

<br>

<p><img src="../../../images/bullet6.png" alt="nokta" align="top"><span class="baslik"> -<b>%s</b>- için son durum</span>
<p><center><table style="width: 90%%;">
<tr>
    <td class="tdh">Dosya</td>
    <td class="tdh">Toplam Mesaj</td>
    <td class="tdh">Çevrilmiş</td>
    <td class="tdh">Belirsiz</td>
    <td class="tdh">Çevrilmemiş</td>
</tr>

'''

htmlBodyTemplate["tr"] = '''<tr>
    <td class="fitd"><a href="%(File-Path)s">%(Project-Id-Version)s</a></td>
    <td class="itd">%(Total)s</td>
    <td class="itd">%(Translated)s</td>
    <td class="itd">%(Fuzzy)s</td>
    <td class="itd">%(Untranslated)s</td>
</tr>'''

htmlFooterTemplate["tr"] = '''
</table></center>
<br>
<br>
<p class="not">
Pardus sayfalarında bulunan bilgi ve belgelerin,
kaynak gösterilmek koşulu ile kullanılması serbesttir.
<em><br>
<strong>TÜBİTAK - UEKAE, PK.74 41470, Gebze / Kocaeli.</strong></em>
Bilgi ve önerileriniz için
<a href="mailto:bilgi%20at%20pardus.org.tr">bilgi at pardus.org.tr</a>
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
