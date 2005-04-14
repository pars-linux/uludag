<?php
  /*
    XMLHTTPRequest örneği
  */
  
  require('class/class.xmlhttprequest.php');

  function toolbar() {
    $arr_toolbar = array();
    $arr_toolbar[] = array('Ana Sayfa', 'home');
    $arr_toolbar[] = array('İletişim', 'contact');
    return $arr_toolbar;
  }
  function load_app($str_app) {
    $arr_apps = array();
    $arr_apps['home'] = "<div>Burası <strong>Ana sayfa</strong></div><br/><form><input type='text2 name='query' value='Aranacak metin' /></form>";
    $arr_apps['contact'] = "<div>Burası <strong>İletişim</strong> sayfası</div><br/>";
    return $arr_apps[$str_app];
  }

  $obj_xhr = new xmlhttprequest();
  $obj_xhr->str_url = 'example.xmlhttprequest.php';
  $obj_xhr->register_func('toolbar', 'cb_toolbar');
  $obj_xhr->register_func('load_app', 'cb_load_app');
  $obj_xhr->handle_request();
?>
<html>
  <head>
    <script>
      function tr_load_app(app) {
        document.getElementById('infobar').innerHTML = 'Lütfen bekleyin...';
        xhr_load_app(app);
      }
      function cb_toolbar(fname, jsobj, req) {
        var s = '';
        for (var k in jsobj) {
          s += '<a href="javascript:tr_load_app(\'' + jsobj[k][1] + '\')">' + jsobj[k][0] + '</a> ';
        }
        document.getElementById('toolbar').innerHTML = s;
      }
      function cb_load_app(fname, jsobj, req) {
        document.getElementById('app').innerHTML = jsobj;
        document.getElementById('infobar').innerHTML = '&nbsp;';
      }
      
      <?php echo $obj_xhr->js_code(true); ?>

      document.onload = xhr_toolbar();
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
