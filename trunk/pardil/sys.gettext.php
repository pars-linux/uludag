<?php
  setlocale(LC_ALL, CONF_LOCALE);
  /*
  bindtextdomain(CONF_DOMAIN, './locales');
  bind_textdomain_codeset(CONF_DOMAIN, 'utf-8');
  textdomain(CONF_DOMAIN);
  */

  require('class.gettext.php');
  require('class.streams.php');

  $res_gettext = new FileReader('locales/' . CONF_LOCALE . '/LC_MESSAGES/' . CONF_DOMAIN . '.mo');
  $obj_gettext = new gettext_reader($res_gettext);

  function __($str_text) {
    global $obj_gettext;
    return $obj_gettext->translate($str_text);
  }

?>
