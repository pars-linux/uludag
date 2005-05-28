<?php
  /*
    Copyright (c) 2005, Bahadır KANDEMİR

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Please read the COPYING file.
  */

  /*
    Tanım:
    ======
    Belirtilen şablon dosyasını kapsüllenmiş olarak çalıştıran sınıf.
    
    Kullanım:
    =========
    $obj_page = new template('tpl.page.php');
    // Argüman olarak gönderilen şablonu kullan.
    
    $obj_page->setvar('myvar1', $my_variable1);
    $obj_page->setvar('myvar2', $my_variable2);
    // Şablon içinde kullanılabilecek değişkenler

    $obj_page->flush();
    // Sayfayı oluştur ve ekrana dök
    
    // echo $obj_name->generate();
    // Ya da sadece oluştur :)

  */
  
  class template {
    private $str_template = '';
    private $arr_variables = array();
    
    function __construct($str_file) {
      $this->str_template = $str_file;
    }
    
    public function setvar($str_name, $mix_value) {
      $this->arr_variables[$str_name] = $mix_value;
    }
    public function generate() {
      global $_PSESSION, $_PCONF;
      foreach ($this->arr_variables as $str_name => $mix_value) {
        $$str_name = $mix_value;
      }
      ob_start();
      include($this->str_template);
      return ob_get_clean();
    }
    public function flush() {
      echo $this->generate();
    }
  }
?>
