<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/


session_start();
$username = $HTTP_POST_VARS[username];
$password = $HTTP_POST_VARS[password];
$result_login = mysql_query("select id, role_id from user where username='$username' and password=PASSWORD('$password')");
if(!mysql_num_rows($result_login))
	$invaliduserpass = true;
else {
	$row_login = mysql_fetch_row($result_login);
	$_SESSION['loggedin'] = 'true';
	$_SESSION['userid'] = $row_login[0];
	$_SESSION['roleid'] = $row_login[1];
}
?>
