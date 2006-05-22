<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */
    
   function search($GETS,$Criteria,$Value){
        global $cf;

        switch ($GETS["act"]){
            case 'answer':
                $sql = "SELECT * FROM {$cf['db']['tableprefix']}Data WHERE {$Criteria}={$Value}"; 
            break;
            default:
                echo 'No criteria given.';
            break;
        }
        
        return perform_sql($sql);
    }

?>
