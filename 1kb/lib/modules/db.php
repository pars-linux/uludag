<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */
    
    /**
     * do_data 
     * 
     * @param string $ID 
     * @param mixed $UID 
     * @param mixed $Tags 
     * @param mixed $Question 
     * @param mixed $RelatedQuestion 
     * @param mixed $Answer 
     * @param mixed $RelatedAnswer 
     * @param mixed $Date 
     * @param int $State 
     * @access public
     * @return void
     */
    function do_data ($ID="x",$UID,$Tags,$Question,$RelatedQuestion,$Answer,$RelatedAnswer,$Date,$State=0)
    {
        global $cf;

        $UID            = rtag($UID);
        $Tags           = rtag($Tags);
        $Question       = rtag($Question);
        $RelatedQuestion= rtag($RelatedQuestion);
        $Answer         = rtag($Answer);
        $RelatedAnswer  = rtag($RelatedAnswer);
        $Date           = rtag($Date);
        $State          = rtag($State);

        if ($ID == "x") 
            $sql = "INSERT INTO {$cf['tb']['Data']} VALUES ('','{$UID}','{$Tags}','{$Question}','{$RelatedQuestion}','{$Answer}','{$RelatedAnswer}','{$Date}','{$State}')";
        elseif ($UID == "delete")
            $sql = "DELETE FROM {$cf['tb']['Data']} WHERE ID={$ID}";
        else
            $sql = "UPDATE {$cf['tb']['Data']} SET UID='{$UID}', Tags='{$Tags}', Question='{$Question}', RelatedQuestion='{$RelatedQuestion}',Answer='{$Answer}',RelatedAnswer='{$RelatedAnswer}',Date='{$Date}',State='{$State}' WHERE ID='$ID'";

        if (@mysql_query($sql))
        {
            if ($ID == "x") 
                return (mysql_insert_id()); 
            else 
                return $ID;
        }
        else 
            show_mysql_errors();
        return FALSE;
    }

    /**
     * do_comment 
     * 
     * @param mixed $ID 
     * @param mixed $UID 
     * @param mixed $DataID 
     * @param mixed $Comment 
     * @param mixed $Date 
     * @param int $State 
     * @access public
     * @return void
     */
    function do_comment ($ID="x",$UID,$DataID,$Comment,$Date,$State=0)
    {
        global $cf;

        $UID            = rtag($UID);
        $DataID         = rtag($DataID);
        $Comment        = rtag($Comment);
        $Date           = rtag($Date);
        $State          = rtag($State);

        if ($ID == "x") 
            $sql = "INSERT INTO {$cf['tb']['Comments']} VALUES ('','{$UID}','{$DataID}','{$Comment}','{$Date}','{$State}')";
        elseif ($UID == "delete")
            $sql = "DELETE FROM {$cf['tb']['Comments']} WHERE ID={$ID}";
        else
            $sql = "UPDATE {$cf['tb']['Data']} SET UID='{$UID}', DataID='{$DataID}', Comment='{$Comment}',Date='{$Date}',State='{$State}' WHERE ID='$ID'";

        if (@mysql_query($sql))
        {
            if ($ID == "x") 
                return (mysql_insert_id()); 
            else 
                return $ID;
        }
        else 
            show_mysql_errors();
        return FALSE;
    }

    /**
     * get_ 
     * 
     * @param string $ID 
     * @param mixed $table 
     * @access public
     * @return void
     */
    function get_($ID="x",$table){
        global $cf;

        if ($table=="UniqUsers")
            $table_real = $cf['db']['users_table'];
        elseif ($table=="pardulDistribution")
            $table_real = $table;
        else 
            $table_real=$cf['db']['tableprefix'].$table;

        if ($ID == "x") 
            $sql = "SELECT * FROM {$table_real}"; 
        else 
            $sql = "SELECT * FROM {$table_real} WHERE ID='{$ID}'";

        return perform_sql($sql);
    }

?>
