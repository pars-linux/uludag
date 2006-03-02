<?
include("config.inc.php");
$SolMenudenGeldi = 0;
include("$AdminAnaDizin/includes/db.inc.php");
include("$AdminAnaDizin/includes/auth.php");
?>
<script>
self.opener.location.replace('/par/pardul/');
</script>
<HTML>
<HEAD>
<TITLE>Yönetim Ana Sayfa</TITLE>
</HEAD>
    <FRAMESET ROWS="100%" COLS="130,*" BORDER="0">
    <FRAME NAME="sol" SRC="<?=$AdminAnaSayfa?>/lib/Menu.php" SCROLLING="AUTO" FRAMEBORDER="0">
    <FRAME NAME="main" SRC="<?=$AdminAnaSayfa?>/index.php" SCROLLING="AUTO" FRAMEBORDER="0">
    </FRAMESET>
</HTML>
