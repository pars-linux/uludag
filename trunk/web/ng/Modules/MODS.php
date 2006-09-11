<?php

    # Set the known values
    $KnownModules = Array ("SVN",
                     "BUGZILLA",
                     "BLOGS",
                     "SCREENSHOTS",
                     "NEWS",
                     "BOX_1",
                     "BOX_2",
                     "BOX_3");

    # Check Module Files
    # if exists include them
    foreach ($KnownModules as $ModFile){
        if (file_exists("Modules/".$ModFile."/".$ModFile."_.php")){
            #echo $ModFile;
            include_once($ModFile."/".$ModFile."_.php");
            $AddedModules[$i++]=$ModFile;
        }
    }

    # Make return values with given Module functions
    function MakeModules($Mod) {
        global $KnownModules,$AddedModules;
        foreach ($AddedModules as $Added)
            global $$Added;
        $Mods = explode (",",trim($Mod,","));
        foreach ($Mods as $MD){
                $TP=$$MD;
                $ReturnValue["Body"].=$TP["Body"];
                $ReturnValue["Head"].=$TP["Head"];
                $ReturnValue["Onload"].=$TP["Onload"];
            }
        return $ReturnValue;
    }

?>
