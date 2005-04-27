<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


$loginForm = new HTML_QuickForm('login_form', 'post', 'dologin.php');
$loginForm->addElement('header', 'header', 'Kullanıcı Girişi');
$loginForm->addElement('text', 'username', 'Kullanıcı Adı:');
$loginForm->addElement('password', 'password', 'Parola:');
$loginForm->addElement('submit', 'btnLogin', 'GİRİŞ');
$renderer =& $loginForm->defaultRenderer();
$loginForm->accept($renderer);
$loginForm->display();
?>
