<?include("config.inc.php");?>
<HTML>
<HEAD>
  <SCRIPT LANGUAGE="JavaScript">
      <!-- Begin
       function popUp(URL) {
       day = new Date();
       id = day.getTime();
       eval("page" + id + " = window.open(URL, '" + id + "', 'toolbar=0,scrollbars=1,location=0,statusbar=1,menubar=0,resizable=0,width=1000,height=690,left = 10,top = 10');");
       }
      // End -->
  </SCRIPT>
</HEAD>
<BODY onLoad="javascript:popUp('<?=$AdminAnaSayfa?>/index.php')">
</BODY>
</HTML>
