<?php
  /*
    XMLHTTPRequest örneği
  */
  
  require('class.xmlhttprequest.php');

  function test1($str_text) {
    echo $str_text;
  }
  function test2($str_text) {
    echo strrev($str_text);
  }
  function test3($str_text) {
    echo strtoupper($str_text);
  }
  function test4($str_text) {
    echo strtolower($str_text);
  }

  $obj_xhr = new xmlhttprequest();
  $obj_xhr->str_url = 'sample.xmlhttprequest.php';
  $obj_xhr->register_func('test1');
  $obj_xhr->register_func('test2');
  $obj_xhr->register_func('test3');
  $obj_xhr->register_func('test4');
  $obj_xhr->handle();
?>
<html>
  <head>
    <script>
      function cb_test1(r) {
        document.getElementById('mytext_s').value = r.responseText;
      }
      function cb_test2(r) {
        document.getElementById('mytext_s').value = r.responseText;
      }
      function cb_test3(r) {
        document.getElementById('mytext_s').value = r.responseText;
      }
      function cb_test4(r) {
        document.getElementById('mytext_s').value = r.responseText;
      }
      <?php echo $obj_xhr->js_code(); ?>
    </script>
  </head>
  <body>
    <input type="text" id="mytext" value="Pardil"/>
    <button onclick="xhr_test1(document.getElementById('mytext').value)">1</button>
    <button onclick="xhr_test2(document.getElementById('mytext').value)">2</button>
    <button onclick="xhr_test3(document.getElementById('mytext').value)">3</button>
    <button onclick="xhr_test4(document.getElementById('mytext').value)">4</button>
    <input type="text" id="mytext_s" readonly="readonly"/>
  </body>
</html>
