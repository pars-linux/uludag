<?php

  /*
    Kullanım:
    $obj_page = new template('tpl.page.php');
    $obj_page->setvar('myvar', $my_variable);
    $obj_page->flush();
    // ya da:
    // echo $obj_name->generate();
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
