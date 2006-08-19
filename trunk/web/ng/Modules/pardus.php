<?php

    class Pardus {

        function Pardus($_DBC) {
            $this->DBC = $_DBC;
        }

        function GetNewsList(){
            $raw =$this->DBC->GetRecord("News","*","","ORDER BY ID DESC LIMIT 5");
            foreach ($raw as $row)
                printf("<a href='#' onClick='get_news(%s);'> %s - %s </a><br>",$row["ID"],$row["Date"],$row["Title"]);
        }

        function GetNews($ID=""){
            $raw =$this->DBC->GetRecord("News","*",$ID,"ORDER BY ID DESC LIMIT 1");
            foreach ($raw as $row)
                printf("<b>%s - %s</b><br> %s",$row["Date"],$row["Title"],$row["Content"]);
        }

        function GetPage($NiceTitle){
            return $this->DBC->FindRecord("Pages","NiceTitle",$NiceTitle,"*","LIMIT 1");
        }

        function GetNiceTitles() {
            return $this->DBC->GetRecord("Pages","NiceTitle");
        }

        function Search($Que) {
            $Que = mysql_escape_string($Que);
            $Results = $this->DBC->GetRecord("Pages","Title,NiceTitle,Content","","WHERE MATCH(Title, Content) AGAINST ('$Que')");
            if (sizeof($Results)>1)
                return $Results;
            else
                return $this->DBC->GetRecord("Pages","Title,NiceTitle,Content","","WHERE (Content LIKE '%$Que%') OR (Title LIKE '%$Que%')");
        }
    }

?>
