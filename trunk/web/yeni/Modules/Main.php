<?php

    $Page = "Main";

    $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
    $known_pages = $Pardus->GetNiceTitles($ActivePage);
    foreach (array_keys($_GET) as $Parameters) {
        foreach ($known_pages as $Pvalues) {
            $Exploded = explode("/",$Parameters);
            if ($Pvalues===$Exploded[0]){
                if (count($Exploded)==2) {
                    foreach($known_pages as $SValues) {
                        if ($SValues===$Exploded[1]){
                            $Page = $Exploded[1];
                            $Parent = $Exploded[0];
                        }
                    }
                }
                else {
                    $Page=$Exploded[0];
                    break;
                }
            }
        }
    }

    $PageContent = $Pardus->GetPage($Page,$ActivePage);
    if ($Parent) $ParentContent = $Pardus->GetPage($Parent,$ActivePage);

?>
