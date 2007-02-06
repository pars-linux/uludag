<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require_once ("functions.php");

    /**
    *    make_*($parameters) it adds or updates a field with given parameters
    *    return Boolean;
    */

    function make_user($uid="x",$realname,$email,$phone,$address,$references,$note,$state='N'){
        global $config;
        $realname       = rtag ($realname);
        $email          = rtag ($email);
        $phone          = rtag ($phone);
        $address        = rtag ($address);
        $references     = rtag ($references);
        $note           = rtag ($note);
        $state          = rtag ($state);
        if ($uid == "x") $sql_word = "INSERT INTO {$config['db']['tableprefix']}Users VALUES ('', '{$realname}', '{$email}','{$phone}', '{$address}', '{$references}', '{$note}', 'N')";
        else $sql_word = "UPDATE {$config['db']['tableprefix']}Users SET UserRealName='{$realname}', UserEmail='{$email}', UserPhone='{$phone}', UserAddress='{$address}', UserReferences='{$references}', UserState='{$state}', UserNote='{$note}' ".$attach_sql." WHERE ID='$uid'";
        return @mysql_query($sql_word);
    }

    /**
    *    get_($table, $field, $value)
    *    it returns a field from $table which $field has $value
    *    return Array;
    */
    function get_($table,$field,$value){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}{$table} WHERE $field = '$value'";
        return perform_sql($sql_word);
    }

    /**
    *    del_($table,$field,$value);
    *    it removes a record from $table which $field has $value
    *    return Boolean;
    */
    function del_($id,$table){
        global $config;
	$sql_word = "DELETE FROM {$config['db']['tableprefix']}{$table} WHERE ID='{$id}'";
        return @mysql_query($sql_word);
    }


    /**
    *    set_($table, $set_field, $set_value, $where_field, $where_value);
    *    it updates a $set_field to $set_value in $table which $where_field has $where_value
    *    return Boolean;
    */
    function set_($table,$sf,$sv,$wf,$wv){
        global $config;
        $sql_word = "UPDATE {$config['db']['tableprefix']}{$table} SET $sf='$sv' WHERE $wf='$wv'";
        return @mysql_query($sql_word);
    }

    function get_products($field="",$value=""){
        global $config;
        if ($field<>"") $add = " WHERE $field = '$value'";
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Hardwares ".$add;
        $single = perform_sql($sql_word);
        if ($single) {
            foreach ($single as $key => $node) {
                $value = $node["UserID"];
                $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Users WHERE ID = '$value'";
                $tmp = mysql_fetch_row(mysql_query($sql_word));
                $single[$key]["UserName"] = $tmp[3];
                $single[$key]["UserEmail"] = $tmp[4];
                $value = $node["ID"];
                $sql_word = "SELECT HWState FROM {$config['db']['tableprefix']}ActionCompatibility WHERE HWID = '$value' AND (HWState = 'F' OR HWState = 'S')";
                $single[$key]["HWState"] = mysql_num_rows(mysql_query($sql_word));
            }
        }
        return $single;
    }

    function sendmail($from,$to,$subject,$message,$priority){
           $mob = new Mail;
           $mob->From($from);
           $mob->To($to);
           $mob->Subject($subject);
           $mob->Body($message, "utf-8");
           $mob->Priority($priority);
           $mob->Send();
    }

    function send_activation_mail($id,$username){
        global $config;
        $activationcode = md5($id.$config["core"]["secretkey"]);
        $mail_message = ACTIVATION_MAIL_HEADER."\n {$config['core']['url']}?activateuser&username={$username}&code={$activationcode}\n".ACTIVATION_MAIL_FOOTER;
        sendmail($config['core']['email'],$_POST["email"],ACTIVATION_MAIL_TITLE,$mail_message,"3");
        return true;
    }

?>
