<?

/*
  Copyright (c) 2005, Faruk Eskicioğlu (farukesk at multi-task.net)

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/
if(GetRoleName($roleid) != "admin") {
	echo "Parametre tanımlamaları için yetkiniz yok.";
	exit;
}
if(isset($subaction))
	require("$subaction.php");
else {
	$menuItems = array(0 => array('title' => 'Pardus Versiyonları', 'url' => '?action=parameters&subaction=pv_param'));
	$to_push = array('title' => 'Model Tanımlamaları', 'url' => '?action=parameters&subaction=model_param');
	array_push($menuItems, $to_push);
	$to_push = array('title' => 'Durum Tanımlamaları', 'url' => '?action=parameters&subaction=status_param');
	array_push($menuItems, $to_push);
	$menu =& new HTML_Menu($menuItems, 'tree');
	$menu->show();
}
?>
