#!/usr/bin/env python
# -*- coding: utf-8 -*-

SITENAME = "Uludağ Haftalık Bülteni"
LOGS = "bultenler"
ARCHIVE = "arsiv"

entry_count = 0 # entries printed in first page

index_file = LOGS + "/.index"
log_prefix = ".txt"

header_text = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
        <title>Ulusal Dağıtım</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico">
        <link rel="stylesheet" href="../style.css" type="text/css">
</head>

<body>
<center>

<div class="frame">

<div class="header">
        <img src="../images/header.png" alt="Uludağ Logo">
</div>

<div class="menubox">
        <a href="../index.html">Ana Sayfa</a> |
        <a href="../kimiz.html">Biz Kimiz?</a> |
        <a href="../projeler.html">Projeler</a> |
        <a href="../belgeler.html">Belgeler</a> |
        <a href="../servisler.html">Servisler</a> |
        <a href="../sorulanlar.html">Sık Sorulanlar</a> |
        <a href="../hakkimizda.html">Hakkımızda</a> |
        <a href="../en/"><font color="red">English</font></a>
</div>

<div class="content">
<!-- ACTUAL PAGE CONTENT START -->
<div class="sayfa">

<p>
Uludağ Haftalık Bülteni, haftalık olarak projeki gelişmeleri bildirmeyi amaçlamaktadır. 
</p>

'''

archive_header = '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
        <title>Ulusal Dağıtım</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico">
        <link rel="stylesheet" href="../../style.css" type="text/css">
</head>

<body>
<center>

<div class="frame">

<div class="header">
        <img src="../../images/header.png" alt="Uludağ Logo">
</div>

<div class="menubox">
        <a href="../../index.html">Ana Sayfa</a> |
        <a href="../../kimiz.html">Biz Kimiz?</a> |
        <a href="../../projeler.html">Projeler</a> |
        <a href="../../belgeler.html">Belgeler</a> |
        <a href="../../servisler.html">Servisler</a> |
        <a href="../../sorulanlar.html">Sık Sorulanlar</a> |
        <a href="../../hakkimizda.html">Hakkımızda</a> |
        <a href="../../en/"><font color="red">English</font></a>
</div>

<div class="content">
<!-- ACTUAL PAGE CONTENT START -->
<div class="sayfa">

'''

footer_text = '''
</div>
<!-- ACTUAL PAGE CONTENT END -->
</div>
</div>

<div class="footer">
        Ulusal Dağıtım CopyLeft 2004
</div>
</center>
</body>
</html>

'''
