<?php
  /*
    XMLHTTPRequest örneği
  */
  
  require('class.xmlhttprequest.php');

  function test1($str_text) {
    return $str_text;
  }
  function test2($str_text) {
    return strrev($str_text);
  }
  function test3($str_text) {
    return strtoupper($str_text);
  }

  $obj_xhr = new xmlhttprequest();
  $obj_xhr->str_url = 'example.xmlhttprequest.php';
  $obj_xhr->register_func('test1', 'cb_test');
  $obj_xhr->register_func('test2', 'cb_test');
  $obj_xhr->register_func('test3', 'cb_test');
  $obj_xhr->handle_request();
?>
<html>
  <head>
    <script>
      function cb_test(fname, jsobj, req) {
        document.getElementById('mytext_s').value = jsobj;
      }
      <?php echo $obj_xhr->js_code(); ?>
    </script>
  </head>
  <body>
    <input type="text" id="mytext" value="Pardil"/>
    <button onclick="xhr_test1(document.getElementById('mytext').value)">1</button>
    <button onclick="xhr_test2(document.getElementById('mytext').value)">2</button>
    <button onclick="xhr_test3(document.getElementById('mytext').value)">3</button>
    <input type="text" id="mytext_s" readonly="readonly"/>
  </body>
</html>
