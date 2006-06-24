<?php

        class Pardus {
           
            private $Connection;
            
            // 0 - to show all states.
            // 2 - to just show errors.
            public $DbLogDetail;

            function DbConnect($DbHost,$DbUser,$DbPass,$DbData){   
                try {
                    $this->Connection = @mysql_connect($DbHost,$DbUser,$DbPass,$DbData);
                    if (!$this->Connection)
                        throw new Exception('Connection Error',2);
                    elseif ($this->DbLogDetail>2)
                        $this->ParseError("Connected to $DbHost::$DbData");
                    mysql_select_db($DbData);
                }

                catch (Exception $Ex) {
                    $this->ShowError($Ex);
                    return 0;
                } 
            }

            function ShowError($Ex,$Note='') { 
                if ($this->DbLogDetail>1) {
                    echo '<pre><b>';
                    echo 'Exception '.$Ex->getCode().' : '.$Ex->getMessage()."<br>";
                    echo 'File        : '.$Ex->getFile().' : '.$Ex->getLine()."<br>";
                    if ($Note<>"") echo 'Note        : '.$Note.'<br>';
                    echo 'Exiting...';
                    echo '</b></pre>';
                }
                else $this->ParseError("An error occured. Exiting..");
            }

            function UpdateField($Table,$Field,$Value,$ID='') {
                $ID == "" ? $AddSql = "" : $AddSql = "WHERE ID=$ID";
                $Sql = "UPDATE $Table SET $Field='$Value' ".$AddSql;
                $this->ExecuteQuery($Sql);               
            }

            function InsertRecord($Table,$Fields,$Values) {
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

            private function ExecuteQuery($Sql) {
                try {
                    $Result = mysql_query($Sql,$this->Connection);
                    if (!$Result)
                        throw new Exception('Query Execution Error',3);
                    elseif ($this->DbLogDetail>2)
                        $this->ParseError("Query Executed Sucessfully : ".$Sql);
                }
                catch (Exception $Ex) {
                    $this->ShowError($Ex,$Sql);
                    return 0;
                }
            }

            function ParseError($Message) {
                echo "<pre><b>".$Message."</b></pre>";
            }
        }

?>
