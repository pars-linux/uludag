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
            $query = "SELECT Title,NiceTitle,Content,MATCH(Title, Content) AGAINST ('$Que' IN BOOLEAN MODE) AS Score FROM Pages WHERE MATCH(Title, Content) AGAINST ('$Que' IN BOOLEAN MODE)";
            echo $query;
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

    function turnTo( $Data,$Lang,$DLang){
        $TR = Array ('İ','Ş','Ğ','Ö','Ü','Ç','ı','ş','ğ','ö','ü','ç');
        $EN = Array ('I','S','G','O','U','C','i','s','g','o','u','c');
        
        foreach($$Lang as $Key=>$Value) {
            $Data = mb_ereg_replace($Value,$$DLang[$Key],$Data,'UTF-8');
        }
        return $Data;
    }
 
    function GetPos($Data,$Word) {
        return mb_strpos(mb_strtolower($Data,'UTF-8'),mb_strtolower($Word,'UTF-8'),0,'UTF-8'); 
    }

    function GetHighlighted($Word,$Data,$Color) {
        return mb_ereg_replace($Word,"<span style='background-color:$Color'>".$Word."</span>",$Data);
    }

    function Highlight($Data,$Word,$Score,$Size=260,$Color="#EDFF88") {
        $Data       = strip_tags($Data);
        $Pos        = GetPos($Data,$Word); 

        if ($Pos==0){ 
            $EnWord = turnTo($Word,'TR','EN');
            $Pos = GetPos($Data,$EnWord);
            if ($Pos==0){
                $TrWord = turnTo($Word,'EN','TR');
                $Pos = GetPos($Data,$TrWord);
            }
        }

        $Piece      = mb_substr($Data,$Pos,$Size*2,'UTF-8');
        $Piece      = GetHighlighted($Word,$Piece,$Color);

        if ($EnWord OR $TrWord) 
            $Piece = GetHighlighted($TrWord,GetHighlighted($EnWord,$Piece,$Color),$Color);         
        #return mb_ereg_replace(mb_strtolower($Word,'UTF-8'),"<span style='background-color:$Color'>".$Word."</span>",mb_strtolower($Piece,'UTF-8'));
        return $Piece;
    }

    if ($_GET["NewsID"]<>""){
        $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
        $Pardus->GetNews($_GET["NewsID"]);
    }

    
?>
