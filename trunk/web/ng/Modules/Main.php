<?php

    if ($Vezir=@new Vezir($CF)){
        $Pardus=new Pardus($Vezir);
        if (isset($_GET["page"])) {

            $BrokenLink = false;
            $KnownPages = $Pardus->GetNiceTitles();

            $CR = __($_GET["page"]);
            if ($CR[strlen($CR)-1]=="/") $CR=rtrim($CR,"/");
            $ER = explode("/",$CR);
            if (false!== array_search($CR,$KnownPages)) {
                $Page = $Pardus->GetPage($CR);
                $Navi = $Pardus->BuildNavi($ER,$Page[0]["Title"]);
                #$Navi = $Page[0]["Title"];
            } else 
                $Navi = WRONG_LINK." : ".$CR;
            # Predefined SideBar Modules, lets start
            if ($Page[0]["Modules"]<>"") {
                include_once("MODS.php");
                $Modules = MakeModules($Page[0]["Modules"]);
            }
        }
    }

?>
