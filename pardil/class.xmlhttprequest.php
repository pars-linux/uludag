<?php

  // XMLHTTPRequest sınıfı


  /*
    Açıklama:
    =========
    PHP'de tanımlı bir fonksiyonu, JS kodu içinden çağırmak gerektiğinde,
    XHR nesnesi yaratılır, yazılan PHP fonksiyonu nesneye tanıtılır. JS kodu 
    içinde 'xhr_<php_fonk_ismi>' fonksiyonu çağrıldığında, ilgili PHP sayfası 
    arkaplanda çağrılır. PHP fonksiyonu çalıştırılır ve 'cb_<php_fonk_ismi>' 
    isimli JS fonksiyonu, PHP fonksiyonundan dönen değer ile çalıştırılır.
    
    Örnek Kullanım:
    ===============
    <?php
      require('class.xmlhttprequest.php');

      function test($str_text) {
        echo strtoupper($str_text);
      }

      $obj_xhr = new xmlhttprequest();
      $obj_xhr->str_url = 'xhr.php';
      $obj_xhr->register_func('test');
      $obj_xhr->handle();
    ?>
     <html>
       <head>
         <script>
           function cb_test(r) {
             alert(r.responseText);
           }
           <?php echo $obj_xhr->js_code(); ?>
         </script>
       </head>
       <body>
         <input type="text" id="mytext" value="merhaba!"/>
         <button onclick="xhr_test(document.getElementById('mytext').value)">Dene!</button>
       </body>
     </html>


     Notlar:
     =======
     XMLHTTPRequest özelliği Mozilla, Opera, Safari, IE gibi tarayıcılar 
     tarafından desteklenmektedir. Yazılan kod, Mozilla'da sorunsuz 
     çalışmaktadır, diğer tarayıcılarda çalışması için ek kod gerekir.
     
     Cross-Browser XMLHTTPRequest desteği için bir JS sınıfı bulunmaktadır, 
     ancak ne yazık ki GPL lisansıyla dağıtılmamaktadır.

     (http://www.scss.com.au/family/andrew/webdesign/xmlhttprequest/)
  */

  class xmlhttprequest {
    public $str_url = '';
    private $arr_functions = array();

    // Gerekli JS kodunu üreten method
    public function js_code() {
      $str_code = 'function xhr_callback(x_f, x_a) {
                     var req = new XMLHttpRequest();
                     if (req) {
                       req.onreadystatechange = function() {
                         if (req.readyState == 4) {
                           if (req.status == 200) {
                             // ok
                             eval(\'cb_\' + x_f + \'(req)\');
                           }
                           else {
                             // error
                           }
                         }
                       };
                       var post = \'op=\' + x_f;
                       for (var i = 0; i < x_a.length; i++) {
                         post += \'&ar[]=\' + x_a[i];
                       }
                       req.open(\'POST\', \'' . $this->str_url .'\');
                       req.setRequestHeader(\'Content-Type\', \'application/x-www-form-urlencoded\');
                       req.setRequestHeader(\'Content-Length\', post.length);
                       req.send(post);
                     }
                   }
                  ';
      foreach ($this->arr_functions as $str_name) {
        $str_code .= sprintf("function xhr_%1\$s() {\nxhr_callback('%1\$s', xhr_%1\$s.arguments);\n}\n", $str_name);
      }
      return $str_code;
    }

    // PHP fonksiyonunu kayıt eden method
    public function register_func($str_name) {
      $this->arr_functions[] = $str_name;
    }

    // XMLHTTPRequest sorgusunu saptayıp gerekli işlemleri yapan method
    public function handle() {
      if (isset($_POST['op']) && in_array($_POST['op'], $this->arr_functions)) {
        call_user_func_array($_POST['op'], $_POST['ar']);
        exit;
      }
    }
  }
?>
