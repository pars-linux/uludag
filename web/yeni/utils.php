<?php

    include_once 'config.php';

    class Pardus {

        var $Connection;

        function Pardus($DbHost,$DbUser,$DbPass,$DbData){
            if ($this->Connection=mysql_connect($DbHost,$DbUser, $DbPass))
                mysql_select_db($DbData,$this->Connection);
            else {
                echo("MySQL Connection Error, Check your settings. Error : ".mysql_error());
                die();
                return 0;
            }
        }

        function GetNewsList(){
            $query = "SELECT ID,Title,Date FROM News ORDER BY DATE DESC LIMIT 5";
            $result= mysql_query($query,$this->Connection);
            while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
                printf("<a href='#' onClick='get_news(%s);'> %s - %s </a><br>", $row["ID"],$row["Date"], $row["Title"]);
            }
            mysql_free_result($result);
        }

        function Search($Que) {
            $query = "SELECT * FROM Pages WHERE (Title LIKE '%{$Que}%') OR (Content LIKE '%{$Que}%')";
            return $this->MakeArray(mysql_query($query,$this->Connection));
        }

        function GetNews($ID=""){
            if ($ID<>"")
                $query = "SELECT * FROM News WHERE ID=$ID";
            else
                $query = "SELECT * FROM News ORDER BY DATE DESC LIMIT 1";
            $result= mysql_query($query,$this->Connection);
            while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
                printf("<b>%s - %s</b><br> %s", $row["Date"], $row["Title"], $row["Content"]);
            }
            mysql_free_result($result);
        }

        function GetPage($NiceTitle="Main",$Parent){
            $query = "SELECT * FROM Pages WHERE NiceTitle='$NiceTitle' AND Parent='$Parent'";
            $result = mysql_query($query,$this->Connection);
            return (mysql_fetch_array($result, MYSQL_ASSOC));
        }

        function GetNiceTitles($ActivePage="") {
            $ActivePage =="" ? $Add ="" : $Add = " WHERE Parent='$ActivePage'";
            $query = "SELECT NiceTitle FROM Pages".$Add;
            return $this->MakeArray(mysql_query($query,$this->Connection),'NiceTitle');
        }

        function MakeArray($Raw,$Field="") {
            $i=0;
            while ($Row = mysql_fetch_array($Raw)) {
                $Field == "" ? $ReturnValue[$i] = $Row : $ReturnValue[$i] = $Row[$Field];
                $i++;
            }
            if ($i==0)
                $ReturnValue = 0;
            mysql_free_result($Raw);
            return $ReturnValue;
        }
    }

    # Search Functions..
    # Begin

    function GiveScore($Data,$Word,$Size=30,$Color="yellow") {

        global $Str;

        $Data       = turnToEn(strip_tags($Data));

        $Len        = strlen($Word);
        $LenData    = strlen($Data);

        $Word       = tolower($Word);

        if ($Size*2 >= $LenData) $Size = round($LenData/2);

        for ($i=0;$i<$LenData;$i+=2) {

            $Piece = substr($Data,$i,$Len);

            if($Word===tolower($Piece)) {

                if ($i>$Size) {
                    $TempData = "...".substr($Data,$i-$Size,$Size).
                    "<span style='background-color:$Color'>".$Piece."</span>".substr($Data,$i+$Len,$Size)."...";
                }

                $j++;

            }

        }

        $ReturnArray['Score'] = $j;
        $ReturnArray['MData'] = $TempData;

        return $ReturnArray;

    }

    function turnToEn( $Data){
        $TrChars = Array ('İ','Ş','Ğ','Ö','Ü','Ç','ı','ş','ğ','ö','ü','ç');
        $EnChars = Array ('I','S','G','O','U','C','i','s','g','o','u','c');
        foreach($TrChars as $Key=>$Value) {
            $Data = preg_replace("#".$Value."#is",$EnChars[$Key],$Data);
        }
        return $Data;
    }

    function tolower($Data) {
        $UpperChars = Array ('İ','Ş','Ğ','Ö','Ü','Ç');
        $LowerChars = Array ('i','ş','ğ','ö','ü','ç');
        foreach($UpperChars as $Key=>$Value) {
            $Data = preg_replace("#".$Value."#is",$LowerChars[$Key],$Data);
        }
        return strtolower($Data);
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

    # Search Functions
    # End

    if ($_GET["NewsID"]<>""){
        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
        $Pardus->GetNews($_GET["NewsID"]);
    }
?>
