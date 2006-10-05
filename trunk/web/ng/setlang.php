<?php

    #define Lang
    if (isset($_GET["lang"]) AND false!==array_search($_GET["lang"],$KnownLangs))
        $AL=$_GET["lang"];
    else
        $AL="tr";

?>
