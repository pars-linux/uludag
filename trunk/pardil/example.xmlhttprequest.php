<?php
  /*
    XMLHTTPRequest örneği
  */
  
  require('class/class.xmlhttprequest.php');

  function toolbar($str_o) {
    $arr_toolbar = array();
    $arr_toolbar[] = array('Ana Sayfa', 'home');
    $arr_toolbar[] = array('İletişim', 'contact');
    return $arr_toolbar;
  }

  $obj_xhr = new xmlhttprequest();
  $obj_xhr->register_func('toolbar');
  $obj_xhr->handle_request();
?>
<html>
  <head>
    <script type="text/javascript" src="class/m_xhr.js"></script>
    <script>
      function tr_toolbar() {
        xhr_php_process('example.xmlhttprequest.php', 'toolbar', '', 'cb_toolbar');
      }
      function cb_toolbar(op, req, obj) {
        var s = '';
        for (var k in obj) {
          s += '<a href="javascript:tr_load_app(\'' + obj[k][1] + '\')">' + obj[k][0] + '</a> ';
        }
        document.getElementById('toolbar').innerHTML = s;
      }
      document.onload = tr_toolbar();
    </script>
  </head>
  <body>
    <div id="toolbar">&nbsp;</div>
    <br/>
    <div id="infobar">&nbsp;</div>
    <br/>
    <div id="app">&nbsp;</div>
  </body>
</html>
