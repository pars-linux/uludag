<?php
  require dirname(__FILE__) . '/json.php';

  class xhr {
    /*
      XHR sınıfı, ilgili sayfaya "POST" edilen anahtar kelime,
      çalıştırılmasına izin verilen fonksiyonlar arasında ise,
      fonksiyonu çalıştıranve çıktısını kullanıcıya gönderen bir
      sınıftır.
    */
    private $fn_php = array();

    public function register($str_php) {
      // İzin verilen fonksiyonları listeye ekleyen fonksiyon
      $this->fn_php[] = $str_php;
    }
    public function handle() {
      /*
        "op" argümanında belirtilen fonksiyon listedeyse,
        fonksiyonu çağır ve çıktısını gönder.
      */
      header("Content-type: text/html; charset=utf-8");
      if (isset($_POST['op']) && in_array($_POST['op'], $this->fn_php)) {
        $obj_json = new JSON(JSON_LOOSE_TYPE);
        $mix_arg = $obj_json->decode($_POST['arg']);
        echo $obj_json->encode(call_user_func($_POST['op'], $mix_arg));
      }
      exit;
    }
  }
?>
