<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<?php

   # Search Module for PW
   # Gökmen GÖKSEL <gokmen _at pardus.org.tr>

   include_once 'utils.php';

   function GiveScore($Data,$Word,$Size=30) {
    mb_internal_encoding("UTF-8");
        $Data = strip_tags($Data);
        $Len  = ztrlen($Word);
        $LenData = ztrlen($Data);
        $j    = 0;
        for ($i=0;$i<$LenData;$i++) {
            $Piece = substr($Data,$i,$Len);
            if(strtolower($Word)===strtolower($Piece)) {
                if ($i>$Size) {
                    $TempData = "...".mb_strcut($Data,$i-$Size,$Size).
                    "<span style='background-color:yellow'>".$Piece."</span>".mb_strcut($Data,$i+$Len,$Size)."...";
                }
                $j++;
            }
        }
        $ReturnArray['Score'] = $j;
        $ReturnArray['MData'] = $TempData;
        return $ReturnArray;
    }

    function array_sort($array, $key, $reverse="") {
        for ($i = 0; $i < sizeof($array); $i++) {
            $sort_values[$i] = $array[$i][$key];
        }
        asort ($sort_values);
        reset ($sort_values);
        while (list ($arr_key, $arr_val) = each ($sort_values)) {
            $sorted_arr[] = $array[$arr_key];
        }
        if ($reverse<>"") return array_reverse($sorted_arr);else return $sorted_arr;
    }

    function ztrlen ($Data) {
        return strlen(utf8_decode($Data));
    }

    if (isset($_GET["q"])) {
        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
        $Results = $Pardus->Search($_GET["q"]);
        $i=0;
        if ($Results) {
            foreach ($Results as $Values) {
                $Temp=GiveScore($Values['Content'],$_GET["q"]);
                if ($Temp['Score']>0) {
                    $Temp['Title']=$Values['Title'];
                    $Sow[$i]=$Temp;
                    $i++;
                }
            }
            if ($i>0) {
                $ReturnValue = array_sort( $Sow,'Score','reverse');
                foreach ($ReturnValue as $Result) {
                    echo "<b>".$Result['Title']." - ".$Result['Score']."</b><br />".$Result['MData']."<br />";
                }
            }
        }
    }

?>
