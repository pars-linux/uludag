<?php

    require_once ('RSS.php');

    $Inst = new RssRead($CF["Modules"]["BLOGS"]["BlogUrl"]);
    $BLOGS["Body"]="\n<div class='img_header'><img src='images/texts/gelistirici_gunlukleri.gif'></div>\n";
    $BLOGS["Body"].=$Inst->ShowList($CF["Modules"]["BLOGS"]["Count"],$CF["Modules"]["BLOGS"]["CharLen"]);

?>
