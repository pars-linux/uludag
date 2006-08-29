<?php

    if ($Vezir=@new Vezir($CF)){
        $Pardus=new Pardus($Vezir);
        if (isset($_GET["page"])) {

            $BrokenLink = false;
            $KnownPages = $Pardus->GetNiceTitles();

            $CR = __($_GET["page"]);
            if ($CR[strlen($CR)-1]=="/") $CR=rtrim($CR,"/");

            $ER = explode("/",$CR);
            if (!array_search($CR,$KnownPages))
                $Navi = WRONG_LINK." : ".$CR;
            else {
                $Page = $Pardus->GetPage($CR);
                $Navi = $Page[0]["Title"];
            }
        }
    }
?>
