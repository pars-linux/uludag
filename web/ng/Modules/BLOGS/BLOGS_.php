<?php

    require_once ('RSS.php');

    $Inst = new RssRead($CF["Modules"]["BLOGS"]["BlogUrl"]);
    $BLOGS["Body"]="\n<img src='images/newdesign/head-gelistirici-gunlukler.png'>\n<br />";
    $BLOGS["Body"].=$Inst->ShowList($CF["Modules"]["BLOGS"]["Count"],$CF["Modules"]["BLOGS"]["CharLen"]);

?>
