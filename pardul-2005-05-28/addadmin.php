<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

?>

<table border="1">
<?
if(GetRoleName($roleid) != "admin") {
	echo "Yönetici tanımlamaları için yetkiniz yok.";
	exit;
}
$formsubmitted = $HTTP_POST_VARS[formsubmitted];
if($formsubmitted) {
	$rname = $HTTP_POST_VARS[rname];
	$email = $HTTP_POST_VARS[email];
	$username = $HTTP_POST_VARS[username];
	$password = $HTTP_POST_VARS[password];
	$role_id = $HTTP_POST_VARS[role_id];
	mysql_query("INSERT INTO `user` ( `id` , `username` , `password` , `rname` , `emailaddr` , `role_id` ) VALUES ('', '$username', PASSWORD('$password'), '$rname', '$email', '$role_id')");
	require("admins.php");
	exit;
}
$addadmin = new HTML_QuickForm('addadmin', 'post', '');
$addadmin->addElement('hidden', 'action', 'addadmin');
$addadmin->addElement('hidden', 'formsubmitted', 'true');
$addadmin->addElement('text', 'rname', 'İsim Soyisim:');
$addadmin->addElement('text', 'email', 'E-Posta:');
$addadmin->addElement('text', 'username', 'Kullanıcı Adı:');
$addadmin->addElement('password', 'password', 'Parola:');
$s =& $addadmin->createElement('select','role_id','Rol: ');
$resultroles = mysql_query("select * from role order by rolename");
while(($rowroles=mysql_fetch_row($resultroles)))
	$opts[$rowroles[0]] = $rowroles[1];
$s->loadArray($opts, $selected);
$addadmin->addElement($s);
$addadmin->addElement('submit', 'btnSave', 'Kaydet');
$addadmin->display();
?>
</table>
