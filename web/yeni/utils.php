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

    if ($_GET["NewsID"]<>""){
        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
        $Pardus->GetNews($_GET["NewsID"]);
    }

?>
