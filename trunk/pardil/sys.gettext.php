<?php
  setlocale(LC_ALL, 'tr_TR');
  bindtextdomain('tr_TR', './l10n');
  bind_textdomain_codeset('tr_TR', 'UTF-8');
  textdomain('tr_TR');

  printf(gettext('Hello!'));
?>
