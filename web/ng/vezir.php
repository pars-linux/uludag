<?php

    // Gökmen GÖKSEL gokmen<at>pardus.org.tr

        class Vezir {

            private $Connection;

            // 0 - to don't show any message.
            // 2 - to just show errors.
            // 3 - to show all actions.
            public $DbLogDetail;

            // Table Prefix
            public $Prefix = "Vezir_";
            public $UsePrefix = True;

            function Vezir($Conf){
                #Set the variables
                $this->DbLogDetail=$Conf["DbLogLevel"];

                if (array_key_exists("Prefix",$Conf))
                    $this->Prefix=$Conf["Prefix"];
                if (array_key_exists("UsePrefix",$Conf))
                    $this->UsePrefix=$Conf["UsePrefix"];

                #Make Connection
                $this->DbConnect($Conf["DbHost"],$Conf["DbUser"],$Conf["DbPass"],$Conf["DbData"]);
            }

            function DbConnect($DbHost,$DbUser,$DbPass,$DbData){
                try {
                    $this->Connection = @mysql_connect($DbHost,$DbUser,$DbPass,$DbData);
                    if (!$this->Connection)
                        throw new Exception('Connection Error',2);
                    elseif ($this->DbLogDetail>3)
                        $this->ParseError("Connected to $DbHost::$DbData");
                    mysql_select_db($DbData);
                }

                catch (Exception $Ex) {
                    $this->ShowError($Ex);
                    exit();
                }
            }

            function ShowError($Ex,$Note='') {
                if ($this->DbLogDetail>1) {
                    echo '<pre><b>';
                    echo 'DEBUG: Exception '.$Ex->getCode().' : '.$Ex->getMessage()."<br>";
                    echo 'DEBUG: File        : '.$Ex->getFile().' : '.$Ex->getLine()."<br>";
                    if ($Note<>"") echo 'DEBUG: Note        : '.$Note.'<br>';
                    echo 'DEBUG: Exiting...';
                    echo '</b></pre>';
                }
                else $this->ParseError("An error occured. Exiting..");
            }

            function UpdateField($Table,$Field,$Value,$ID='') {
                $Table=$this->Pref_($Table);
                $ID == "" ? $AddSql = "" : $AddSql = "WHERE ID=$ID";
                $Sql = "UPDATE $Table SET $Field='$Value' ".$AddSql;
                $this->ExecuteQuery($Sql);
            }

            function Pref_($Table) {
                if ($this->UsePrefix==true)
                    return $this->Prefix.$Table;
                return $Table;
            }

            function UpdateArray($Table,$Fields,$Values,$ID) {
                $Table=$this->Pref_($Table);
                if ($ID) {
                    $Sql = "UPDATE $Table SET ";
                    foreach ($Fields as $Key=>$Field)
                        $Sql .= $Field."='".$Values[$Key]."',";
                    $Sql = rtrim($Sql,",")." WHERE ID=".$ID;
                    if ($this->ExecuteQuery($Sql)) return true;
                }
                return false;
            }

            function InsertRecord($Table,$Fields,$Values) {
                $Table=$this->Pref_($Table);
                $Sql = "INSERT INTO $Table (";
                foreach ($Fields as $FValue) {
                    $Sql .= $FValue.",";
                }
                $Sql = rtrim($Sql,",");
                $Sql .= ") VALUES (";
                foreach ($Values as $VValue) {
                    $Sql .= "'".$VValue."'".",";
                }
                $Sql = rtrim($Sql,",");
                $Sql .=")";
                $this->ExecuteQuery($Sql);
                return mysql_insert_id();
            }

            function DeleteRecord($Table,$ID) {
                $Table=$this->Pref_($Table);
                $Sql = "DELETE FROM $Table WHERE ID=$ID";
                return $this->ExecuteQuery($Sql);
            }

            protected function ExecuteQuery($Sql) {
                try {
                    $Result = mysql_query($Sql,$this->Connection);
                    if (!$Result)
                        throw new Exception('Query Execution Error',3);
                    elseif ($this->DbLogDetail>2){
                        if (strlen($Sql)>100) $Sql = substr($Sql, 0, 90)."...";
                        $this->ParseError("Query Executed Sucessfully : ".$Sql);
                    }
                    return $Result;
                }
                catch (Exception $Ex) {
                    $this->ShowError($Ex,$Sql);
                    return false;
                }
            }

            function ParseError($Message) {
                $this->MessageQueue.= "<pre><b>DEBUG : ".$Message."</b></pre>";
            }

            function GetRecord($Table,$Field='*',$ID='',$Ext='') {
                $Table=$this->Pref_($Table);
                $ID == "" ? $AddSql = "" : $AddSql = "WHERE ID=$ID";
                $Ext == "" ? $AddSql = $AddSql: $AddSql = $AddSql." ".$Ext;
                $Sql = "SELECT $Field FROM $Table ".$AddSql;
                $Result = $this->ExecuteQuery($Sql);
                return $this->MakeArray($Result);
            }

            function FindRecord($Table,$Field,$Value,$ReturnValue='ID',$Ext='') {
                $Table=$this->Pref_($Table);
                $Ext == "" ? $AddSql = "": $AddSql = $Ext;
                $Sql = "SELECT $ReturnValue FROM $Table WHERE $Field LIKE '%$Value%' ".$AddSql;
                $Result = $this->ExecuteQuery($Sql);
                return $this->MakeArray($Result);
            }

            function MakeArray($Raw) {
                $i=0;
                while ($Row = mysql_fetch_array($Raw, MYSQL_ASSOC)) {
                    foreach ($Row as $RKey => $RValue)
                        $ReturnValue[$i][$RKey] = $RValue;
                    $i++;
                }
                if ($i==0)
                    $ReturnValue = 0;
                mysql_free_result($Raw);
                return $ReturnValue;
            }

            function ShowLogs($Opt=0) {
                if ($Opt)
                    return $this->MessageQueue;
                else
                    echo $this->MessageQueue;
            }

            function GetUserDetails($Table,$UserName,$PassWord,$Plain=true) {
                $Table=$this->Pref_($Table);
                if ($Plain) $PassWord = md5($PassWord);
                $Sql="SELECT * FROM $Table WHERE (UserName='{$UserName}') AND (Password='{$PassWord}')";
                $Result = $this->ExecuteQuery($Sql);
                if ($Result)
                    return $this->MakeArray($Result);
                return false;
            }

        }

?>
