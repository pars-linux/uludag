<?php
   
     /*
         TUBITAK UEKAE 2005-2006
         Gökmen GÖKSEL gokmen_at_pardus.org.tr
     */
   
     /**
      * get_user_details 
      * 
      * @param mixed $user 
      * @param mixed $pass 
      * @param string $state 
      * @access public
      * @return void
      */
     function get_user_details($user,$pass,$state="x")
     {
        global $config;
        $passx  = md5($pass);
        $state = "x" ? $attach_sql ="AND UserState != 'N'" : $attach_sql ="AND UserState = '{$state}'";
        $sql = "SELECT * FROM {$config['db']['users_table']} WHERE UserName = '$user' AND UserPass = '$passx' ".$attach_sql;
        return perform_sql($sql);
     }
    
    /**
     * get_user 
     * 
     * @param mixed $field 
     * @param mixed $value 
     * @access public
     * @return void
     */
    function get_user($field,$value)
    {
        global $config;
        $sql = "SELECT * FROM {$config['db']['users_table']} WHERE $field = '$value'";
        return perform_sql($sql);
    }

    /**
     * sendmail 
     * 
     * @param mixed $from 
     * @param mixed $to 
     * @param mixed $subject 
     * @param mixed $message 
     * @param mixed $priority 
     * @access public
     * @return void
     */
    require_once ('mail.php');
    function sendmail($from,$to,$subject,$message,$priority)
    {
           $mob = new Mail;
           $mob->From($from);
           $mob->To($to);
           $mob->Subject($subject);
           $mob->Body($message, "utf-8");
           $mob->Priority($priority);
           $mob->Send();
    }

    /**
     * activate_user 
     * 
     * @param mixed $username 
     * @param mixed $code 
     * @param string $action 
     * @access public
     * @return void
     */
    function activate_user($username,$code,$action="activate")
    {
        global $config;
        $node = get_user("UserName",$username);
        if ($node[0]["UserState"] == "N") {
            if(md5($node[0]["ID"].$config["core"]["secretkey"]) == $code){
                if($action == "activate"){
                    $sql = "UPDATE {$config['db']['users_table']} SET UserState='SA' WHERE ID='{$node[0]["ID"]}' LIMIT 1";
                    if (@mysql_query($sql)) 
                        return ACTIVATE_USER_OK; 
                    else 
                    {
                        show_mysql_errors();
                        return ACTIVATE_USER_ERROR;
                    }
                }
            }
            else {
                return ACTIVATE_USER_ERROR;
            }
        }
        else return ACTIVATED_USER;
    }

    /**
     * send_activation_mail 
     * 
     * @param mixed $id 
     * @param mixed $username 
     * @access public
     * @return void
     */
    function send_activation_mail($id,$username)
    {
        global $config;
        $activationcode = md5($id.$config["core"]["secretkey"]);
        $mail_message   = ACTIVATION_MAIL_HEADER."\n {$config['core']['url']}?activate&username={$username}&code={$activationcode}\n".ACTIVATION_MAIL_FOOTER;
        if (sendmail($config['core']['email'],$_POST["email"],ACTIVATION_MAIL_TITLE,$mail_message,"3"))
            return MAIL_SEND_OK;
        else
            return MAIL_SEND_FAILED;
    }

?>
