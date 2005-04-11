<?php

  // XMLHTTPRequest sınıfı


  /*
    Açıklama:
    =========
    PHP'de tanımlı bir fonksiyonu, JS kodu içinden çağırmak gerektiğinde,
    XHR nesnesi yaratılır, yazılan PHP & JS fonksiyonları nesneye tanıtılır. 
    JS kodu içinde 'xhr_<php_fonk_ismi>' fonksiyonu çağrıldığında, ilgili PHP 
    sayfası arkaplanda çağrılır. PHP fonksiyonu çalıştırılır ve tanıtılan JS  
    JS fonksiyonu, PHP fonksiyonundan dönen değer ile çalıştırılır.
    
    Örnek Kullanım:
    ===============
    http://haftalik.net/classes/xhr/example.xmlhttprequest.phps

    Notlar:
    =======
    XMLHTTPRequest özelliği Mozilla, Opera, Safari, IE gibi tarayıcılar 
    tarafından desteklenmektedir. Yazılan kod, Mozilla'da sorunsuz 
    çalışmaktadır, diğer tarayıcılarda çalışması için ek kod gerekir.
     
    Cross-Browser XMLHTTPRequest desteği için bir JS sınıfı bulunmaktadır, 
    ancak ne yazık ki GPL lisansıyla dağıtılmamaktadır.

    (http://www.scss.com.au/family/andrew/webdesign/xmlhttprequest/)
  */

  require('class/class.json.php');

  class xmlhttprequest {
    public $str_url = '';
    private $arr_functions_php = array();
    private $arr_functions_js = array();

    // Gerekli JS kodunu üreten method
    public function js_code($bln_common=true) {
      $str_code = '';
      if ($bln_common) {
        $str_code = 'function xhr_escape(str_in) {
                       var str_out = \'\';
                       for (var i = 0; i < str_in.length; i++) {
                         if (( 33 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 47) || (58 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 64) || (91 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 96) || (123 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 127)) {
                           str_out += escape(str_in.charAt(i));
                         }
                         else {
                           str_out += str_in.charAt(i);
                         }
                       }
                       return str_out;
                     }
                     function xhr_callback(x_php, x_js, x_arg) {
                       var req = new XMLHttpRequest();
                       if (req) {
                         req.onreadystatechange = function() {
                           if (req.readyState == 4) {
                             if (req.status == 200) {
                               // ok
                               jsobjstr = req.responseText;
                               eval(\'window.jsobj = \' + jsobjstr);
                               eval(x_js + \'(x_php, jsobj, req)\');
                             }
                             else {
                               // error
                             }
                           }
                         };
                         var post = \'op=\' + x_php;
                         for (var i = 0; i < x_arg.length; i++) {
                           post += \'&arg[]=\' + xhr_escape(x_arg[i]);
                         }
                         req.open(\'POST\', \'' . $this->str_url .'\');
                         req.setRequestHeader(\'Content-Type\', \'application/x-www-form-urlencoded\');
                         req.setRequestHeader(\'Content-Length\', post.length);
                         req.send(post);
                       }
                     }
                    ';
      }
      for ($i = 0; $i < count($this->arr_functions_php); $i++) {
        $str_f_php = $this->arr_functions_php[$i];
        $str_f_js = $this->arr_functions_js[$i];
        $str_code .= sprintf("function xhr_%1\$s() {\nxhr_callback('%1\$s', '%2\$s', xhr_%1\$s.arguments);\n}\n", $str_f_php, $str_f_js);
      }
      return $str_code;
    }

    // PHP fonksiyonunu kayıt eden method
    public function register_func($str_php_func, $str_js_func) {
      $this->arr_functions_php[] = $str_php_func;
      $this->arr_functions_js[] = $str_js_func;
    }

    // XMLHTTPRequest sorgusunu saptayıp gerekli işlemleri yapan method
    public function handle_request() {
      if (isset($_POST['op']) && in_array($_POST['op'], $this->arr_functions_php)) {
        $obj_json = new JSON();
        $str_obj = call_user_func_array($_POST['op'], $_POST['arg']);
        echo $obj_json->encode($str_obj);
        exit;
      }
    }
  }
?>
