<?php
  setlocale(LC_MESSAGES, CONF_LOCALE);

  require(dirname(__FILE__) . '/../class/class.gettext.php');
  require(dirname(__FILE__) . '/../class/class.streams.php');

  $res_gettext = new FileReader(dirname(__FILE__) . '/../locales/' . CONF_LOCALE . '/LC_MESSAGES/' . CONF_DOMAIN . '.mo');
  $obj_gettext = new gettext_reader($res_gettext);

  function __($str_text) {
    global $obj_gettext;
    return $obj_gettext->translate($str_text);
  }
  
  function __e($str_text) {
    global $obj_gettext;
    echo $obj_gettext->translate($str_text);
  }

?>
