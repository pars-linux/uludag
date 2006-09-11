<?php

    require_once ('RSS.php');

    $Inst = new RssRead($CF["Modules"]["BLOGS"]["BlogUrl"]);
    $BLOGS["Body"]="\n
    <img src='images/newdesign/head-gelistirici-gunlukler.png'>\n<div id='RssList'>";
    $BLOGS["Body"].=$Inst->ShowList($CF["Modules"]["BLOGS"]["Count"],$CF["Modules"]["BLOGS"]["CharLen"]);
    $BLOGS["Body"].="</div>";
?>
