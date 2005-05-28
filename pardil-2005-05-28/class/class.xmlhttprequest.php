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

  require(dirname(__FILE__) . '/class.json.php');

  class xmlhttprequest {
    public $str_url = '';
    private $arr_functions_php = array();

    // PHP fonksiyonunu kayıt eden method
    public function register_func($str_php_func) {
      $this->arr_functions_php[] = $str_php_func;
    }

    // XMLHTTPRequest sorgusunu saptayıp gerekli işlemleri yapan method
    public function handle_request() {
      if (isset($_POST['op']) && in_array($_POST['op'], $this->arr_functions_php)) {
        $obj_json = new JSON(JSON_LOOSE_TYPE);
        $str_obj = call_user_func($_POST['op'], $obj_json->decode($_POST['arg']));
        echo $obj_json->encode($str_obj);
        exit;
      }
    }
  }
?>
