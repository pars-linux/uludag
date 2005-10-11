<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title>$site_title</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
    <!--
    <link rel="icon" type="image/png" href="images/favicon.png"/>
    <link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="feed.rss" />
    -->
    <script type="text/javascript">
      // <![CDATA[
      function post_to_window(form, name, url) {
        form = document.getElementById(form);
        window.open(url, name, 'width=750,height=700,left=50,top=5,screenX=50,screenY=50');
        form.target = name;
        form.action = url
        form.submit()
      }
      // ]]>
    </script>
  </head>
  <body>
    <div id="container">
      <div id="header">
        <a href="index.py"><h1>$site_title</h1></a>
      </div>
      <div id="menu">
        #include $site_path + "templates/menu.tpl"
      </div>
