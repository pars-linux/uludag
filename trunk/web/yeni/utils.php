<?php
    
    // Utils.php, tools for pardus.org.tr
    
    /* Forget it , use MySQL
    class NewsReader {
        
        // Gets the file name for News in XML Format.
        var $NewsFile;
        var $FilePointer;
        var $Content;

        function NewsReader($NewsFilePath){
            $this->NewsFile = $NewsFilePath;
            
            if ($this->FilePointer = fopen($this->NewsFile,"r"))
                $this->Content = fread($this->FilePointer,filesize($this->NewsFile));
            else {
                echo "<b>File Not Found !... </b>";
                $this->FilePointer = fopen($this->NewsFile,"w");
                echo "<b> Created at $NewsFilePath </b> Note: Refresh ;) ";
            }
        }
    }

    */

    class Pardus {

        var $DbHost = "127.0.0.1";
        var $DbUser = "root";
        var $DbPass = "gooksel";
        var $DbData = "Pardus";
        var $Connection; 
   
        function Pardus(){
            if ($this->Connection=mysql_connect($this->DbHost,$this->DbUser, $this->DbPass))
                mysql_select_db($this->DbData,$this->Connection);
            else {
                echo("MySQL Connection Error, Check your settings. Error : ".mysql_error());
                return 0;
            }
        }

        function GetNewsList(){
            $query = "SELECT Title,Date FROM News ORDER BY DATE DESC LIMIT 5";
            $result= mysql_query($query,$this->Connection);
            while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
                printf("%s - %s <br>", $row["Date"], $row["Title"]);
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

    }

    
?>
