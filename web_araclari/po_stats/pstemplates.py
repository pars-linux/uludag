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
                            <tr><td>%(Project-Name)s, %(File-Name)s</td><td>%(Total)s</td><td>%(Translated)s</td><td>%(Fuzzy)s</td><td>%(Untranslated)s</td></tr>
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
        <title>:: Pardus :: TÜBİTAK-UEKAE ::</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link href="../../../../style.css" rel="stylesheet" type="text/css">
        <link rel="shortcut icon" type="image/x-icon" href="../../../../images/favicon.ico">

        <style type="text/css">
            .tdh {
                text-align: center;
                font-weight: bold;
                background-color: #DDD;
                border-bottom: 1px #000 solid;
            }

            .itd {
                text-align: center;
            }

            .fitd {
            }

        </style>
</head>

<body>
<div id="container">
    <div id="head_grey2">
        <div id="blue2">
        <map name="header_map">
        <area shape="rect" href="index.html" coords="24,24,143,101" >
        <area shape="rect" href="documents/HOWTO_install.html" coords="596,115,721,144" >
        <area shape="rect" href="download.html" coords="596,26,721,105" >
        </map>
        <img src="../../../images/header.png" usemap="#header_map" width="740" height="163" border="0">
        </div>
    </div>
    <div id="navi">
        <a href="../../../index.html">Home</a>
      | <a href="../../../info.html">About</a>
      | <a href="../../../projects/index.html">Projects</a>
      | <a href="../../../documents/index.html">Documents</a>
      | <a href="../../../products/index.html">Products</a>
      | <a href="../../../contact.html">Contact Us</a>
      | <a href="../../../press/index.html">Press</a>
      | <a href="../../../../index.html">Türkçe</a>
    </div>
    <div id="page" class="blue2">
        <div id="mainpage">


<p><img src="../../../images/bullet6.png" alt="nokta" align="top"><span class="baslik"> Po stats for -<b>%s</b>-</span>

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
    <td class="fitd"><a href="%(File-Path)s">%(Project-Name)s</a></td>
    <td class="itd">%(Total)s</td>
    <td class="itd">%(Translated)s</td>
    <td class="itd">%(Fuzzy)s</td>
    <td class="itd">%(Untranslated)s</td>
</tr>
<tr>
    <td colspan="5" style="width: 100%%; border-bottom: 1px #000 solid;">
        <table style="width: 100%%; height: 6px; margin: 0px; padding: 0px;">
            <tr>
                <td style="width: %(pT)s%%; padding: 0px; margin: 0px; background-color: #62cf62;"></td>
                <td style="width: %(pF)s%%; padding: 0px; margin: 0px; background-color: #d8ea42;"></td>
                <td style="width: %(pU)s%%; padding: 0px; margin: 0px; background-color: #ea4242;"></td>
            </tr>
        </table>
    </td>
</tr>

'''

htmlFooterTemplate["en"] = '''
</table></center>
<br>
        <div id="footnote">
            <p>
              Information and documents on Pardus web pages can be used freely anywhere with original source credit.<br />
              For information and suggestion(s) please write to <a href="mailto:bilgi%20at%20pardus.org.tr">bilgi_at_pardus.org.tr</a><br />
              <em>TÜBİTAK - UEKAE, PK.74 41470, Gebze / Kocaeli.</em>
           </p>
        </div>

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
   <title>:: Pardus :: TÜBİTAK-UEKAE ::</title>
   <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <link href="../../../style.css" rel="stylesheet" type="text/css">
   <link rel="shortcut icon" type="image/x-icon" href="../../../images/favicon.ico">


        <style type="text/css">
            .tdh {
                text-align: center;
                font-weight: bold;
                background-color: #DDD;
                border-bottom: 1px #000 solid;
            }

            .itd {
                text-align: center;
            }

            .fitd {
            }

        </style>

</head>
<body>
<div id="container">
    <div id="head_grey2">
        <div id="blue2">
        <map name="header_map">
        <area shape="rect" href="index.html" coords="24,24,143,101" >
        <area shape="rect" href="belgeler/kurulum_nasil.html" coords="596,115,721,144" >
        <area shape="rect" href="indir.html" coords="596,26,721,105" >
        </map>
        <img src="images/header.png" usemap="#header_map" width="740" height="163" border="0">
      </div>
    </div>
    <div id="navi">
        <a href="../../../index.html">Ana Sayfa</a>
      | <a href="../../../urunler/index.html">Ürünler</a>
      | <a href="../../../projeler/index.html">Projeler</a>
      | <a href="../../../belgeler/index.html">Belgeler</a>
      | <a href="../../../hakkimizda.html">Hakkımızda</a>
      | <a href="../../../basin/index.html">Basın Odası</a>
      | <a href="../../../iletisim.html">İletişim</a>
      | <a href="../../../eng/index.html">English</a>
    </div>
    <div id="page" class="blue2">
        <div id="mainpage">

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

htmlBodyTemplate["tr"] = '''
<tr>
    <td class="fitd"><a href="%(File-Path)s">%(Project-Name)s</a></td>
    <td class="itd">%(Total)s</td>
    <td class="itd">%(Translated)s</td>
    <td class="itd">%(Fuzzy)s</td>
    <td class="itd">%(Untranslated)s</td>
</tr>
<tr>
    <td colspan="5" style="width: 100%%; border-bottom: 1px #000 solid;">
        <table style="width: 100%%; height: 6px; margin: 0px; padding: 0px;">
            <tr>
                <td style="width: %(pT)s%%; padding: 0px; margin: 0px; background-color: #62cf62;"></td>
                <td style="width: %(pF)s%%; padding: 0px; margin: 0px; background-color: #d8ea42;"></td>
                <td style="width: %(pU)s%%; padding: 0px; margin: 0px; background-color: #ea4242;"></td>
            </tr>
        </table>
    </td>
</tr>

'''

htmlFooterTemplate["tr"] = '''
</table></center>
<br>
        <div id="footnote">
            <p>
               Bu web sitesinde bulunan bilgi ve belgelerin, kaynak gösterilmek koşulu ile kullanılması serbesttir.<br />
               Pardus markası ve logotipi TÜBİTAK'ın tescilli markasıdır. Kullanım koşulları için <a href="yasal_uyari.html">Yasal Uyarı</a> bölümünü inceleyiniz.<br />·
               Bilgi ve önerileriniz için <a href="mailto:bilgi%20at%20pardus.org.tr">bilgi at pardus.org.tr</a>
               <em>TÜBİTAK - UEKAE, PK.74 41470, Gebze / Kocaeli.</em>
            </p>
        </div>
    </div>

</td>
</tr>
</table>

</td>
</tr>
</table>

</body>
</html>

'''
