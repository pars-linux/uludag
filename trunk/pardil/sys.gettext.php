<?php
  setlocale(LC_MESSAGES, CONF_LOCALE);

  require('class.gettext.php');
  require('class.streams.php');

  $res_gettext = new FileReader('locales/' . CONF_LOCALE . '/LC_MESSAGES/' . CONF_DOMAIN . '.mo');
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
