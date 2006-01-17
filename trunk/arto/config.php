<?php
// Core Config
$config['core']['title']		= "sanat.pardus";
$config['core']['desc']			= "Arto yeni sanat o ..";
$config['core']['path']			= "/home/rat/public_html/arto/";
$config['core']['url']			= "http://localhost/~rat/arto/";
$config['core']['postperpage']		= "5";
$config['core']['postsinfeed']		= "10";
$config['core']['theme']		= "zirto";
$config['core']['temp']			= "tmp";
$config['core']['lang']			= "tr";

// DB Config for MySQL
$config['db']['hostname']		= "localhost";
$config['db']['port']			= "3306";
$config['db']['username']		= "root";
$config['db']['password']		= "goksel";
$config['db']['databasename']		= "uludag";
$config['db']['tableprefix']		= "arto_";
$config['db']['connectiontype']		= "persistent";

// Smarty Config
$config['smarty']['libdir']		= "3rdparty/smarty";
$config['smarty']['tpldir']		= "themes";
$config['smarty']['compiledir']		= "tmp";
$config['smarty']['cachedir']		= "tmp";
$config['smarty']['plugindir']		= "plugins";
$config['smarty']['caching']		= "false";
$config['smarty']['forcecompile']	= "1";

// Arto Config
$config['arto']['version']		= "0.1";
$config['arto']['builddate']		= "20060114";
?>
