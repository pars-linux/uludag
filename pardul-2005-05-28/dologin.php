<?
include("inc/functions.inc.php");
require_once 'HTML/QuickForm.php';
require_once "HTML/Table.php";
require_once 'HTML/Menu.php';

$dsn = MYSQLConnect();

$username = $HTTP_POST_VARS[username];
$password = $HTTP_POST_VARS[password];

$result_login = mysql_query("select id, role_id from user where username='$username' and password=PASSWORD('$password')");
if(!mysql_num_rows($result_login)) {
	addPageHeader($title);
	echo "
	<table widt=\"80%\" border=\"1\">
		<tr>
			<td colspan=\"2\" align=\"center\">
			<a href=\"?action=login\">Yönetici</a>
		</td>
	</tr>
	<tr>
		<td align=\"left\" valign=\"top\" width=\"10%\">
		PARDUL
	</td>
	<td align=\"center\" valign=\"top\" width=\"90%\">
		<table>
			<tr>
				<td align=\"center\">
	";
	$loginForm = new HTML_QuickForm('login_form', 'post', 'dologin.php');
	$loginForm->addElement('header', 'header', 'Kullanıcı Girişi');
	$loginForm->addElement('text', 'username', 'Kullanıcı Adı:');
	$loginForm->addElement('password', 'password', 'Parola:');
	$loginForm->addElement('submit', 'btnLogin', 'GİRİŞ');
	echo "Girdiğiniz kullanıcı adı ve/veya parola yanlış.<br>";
	$renderer =& $loginForm->defaultRenderer();
	$loginForm->accept($renderer);
	$loginForm->display();
	echo "
	</tr>
	</table>
	";
	addPageFooter();
}
else {
	session_start();
	$row_login = mysql_fetch_row($result_login);
	$_SESSION['loggedin'] = 'true';
	$_SESSION['userid'] = $row_login[0];
	$_SESSION['roleid'] = $row_login[1];
	header("Location: $APPL_URL");
}
mysql_close();
?>
