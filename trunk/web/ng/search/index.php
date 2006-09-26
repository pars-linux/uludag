<?php

    // TUBITAK/UEAKE - 2006-07 - Pardus
    // Gökmen GÖKSEL <gokmen@pardus.org.tr>
    // Search in Pardus DataBase

    include_once '../config.php';
    include_once '../vezir.php';
    include_once 'search.php';
    include_once "../langs/tr.php";

    if (isset($_GET["q"]) or isset($_GET["r"])) {

        $Vezir  = new Vezir($CF);
        #$Vezir->LimitedLog=false;
        $Pardus = new Pardus($Vezir);
        $SearchWord = __($_GET["q"]);

        if (isset($_GET["page"]))
            $Page = $Pardus->GetPage(__($_GET["page"]));
        else {
            if (strlen($SearchWord)>3) {
                $Results = $Pardus->Search($SearchWord);
                $Search = new Sud($Results,$SearchWord);
            }
            else
                $Message = ERROR_SEARCH_WORD_AT_LEAST_FOUR_CHARACTER;
        }
    }

?>
<!DOCTYPE html
     PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="tr" xml:lang="tr">
<head>
    <title><?=PAGE_TITLE?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link href="../style.css" rel="stylesheet" type="text/css">

    <script>

        allPageTags = new Array();
        colorValues = new Array();
        contact     = 1;

        function init() {
            allPageTags=document.getElementsByTagName("*");
            for (i=0; i<allPageTags.length; i++) {
                var node = allPageTags[i].className.split("_");
                if (node[0]=="r") {
                    colorValues[node[1]] = allPageTags[i].style.background;
                }
            }

        }

        function HideHighlights() {
            for (i=0; i<allPageTags.length; i++) {
                if (allPageTags[i].className.split("_")[0]=="r") {
                    allPageTags[i].style.background='none';
                }
            }
        }

        function ToggleHighlights(src) {
            for (i=0; i<allPageTags.length; i++) {
                var node = allPageTags[i].className.split("_");
                if (node[0]=="r") {
                    if (contact==0)
                        allPageTags[i].style.background=colorValues[node[1]];
                    else
                        allPageTags[i].style.background='none';
                }
            }

            var str = src.innerHTML;

            if (contact==1) {
                src.innerHTML = str.replace(/<?=HIDEHIGHLIGHT?>/, "<?=SHOWHIGHLIGHT?>");
                contact=0;
            }
            else {
                 src.innerHTML = str.replace(/<?=SHOWHIGHLIGHT?>/, "<?=HIDEHIGHLIGHT?>");
                contact=1;
            }
        }
    </script>

</head>

<body onload="init();">
 <div id="container">

    <div id="head_grey">
        <div id="blue2"></div>
        <div id="quick_download">
            <img src="../images/box-hizli-indir.png" alt="Pardus 1.1Beta"/>
            <form action="">
                <input type="text" name="q" id="search" value="<?=SEARCH?>" onclick="Javascript:if (this.value=='<?=SEARCH?>') this.value='';" onblur="Javascript:if (this.value=='') this.value='<?=SEARCH?>';"/>
            </form>
        </div>
    </div>

    <div id="navi">
        <a href="../"><?=MAIN_PAGE?></a> 
        <?php
            if (isset($Search)) 
                echo " » '".$SearchWord."' ".SEARCHED;
            elseif (isset($Page))
                echo " » <a href='$PHP_SELF?q=$SearchWord'> '".$SearchWord."' ".RESULTS."</a> » ".$Page[0]["Title"];
        ?>
    </div>

    <div id="fullpage">
    <?php
        if (isset($Page))
            echo $Page[0]["Content"];
        else {
            #$Vezir->ShowLogs();
            if (isset($Search)) {
                echo "<div class='info'>";
                if ($Results[0]['NiceTitle']<>"") {
                    echo TOTAL."<b>".sizeof($Results)."</b>".RECORD_FOUND_ALSO_YOU_CAN_LOOK_AT_GOOGLE_RESULTS;
                    echo "<a href=# onClick='ToggleHighlights(this);return false'>".HIDEHIGHLIGHT."</a> <br/>";
                }
                else 
                    echo NO_RECORD_FOUND_BUT_YOU_CAN_LOOK_AT_GOOGLE_RESULTS;
                echo "</div>";
                if ($Results)
                    $Search->Mod1();
                }
                elseif (isset($Message))
                    echo "<div class='info'>".$Message."</div>";
        }
    ?>
    </div>
    <div id="footnote"><p><?=PARDUS_REGISTER?></p></div>
 </div>
</body>
</html>
