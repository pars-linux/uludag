<?php

    function db_connection($action, $dbhost = "", $dbuser = "", $dbpass = "", $dbname = "", $dbconntype = ""){
        global $db_connection;

        if($action == "connect"){
            if($dbconntype == "persistent"){$db_connection = @mysql_pconnect($dbhost, $dbuser, $dbpass);}
            elseif($dbconntype == "nonpersistent"){$db_connection = @mysql_connect($dbhost, $dbuser, $dbpass);}
            else{$db_connection = @mysql_connect($dbhost, $dbuser, $dbpass);}

            if(!$db_connection){ show_mysql_errors(); exit();}
            $db_select = @mysql_select_db($dbname);

            if(!$db_select){ show_mysql_errors(); exit();}
        }

        elseif($action == "disconnect"){mysql_close($db_connection);}
    }

    /*
        show_mysql_errors()
        It shows nice mysql errors
        return No_Return;
    */
    function show_mysql_errors() {
            echo DBCONERROR."<br>";
            echo ERRORMESSAGE."<b>".mysql_error()."</b><br>";
            echo ERRORNUM."<b>".mysql_errno()."</b><br>";
    }

    function perform_sql($sql_word){
            $sql_query = mysql_query($sql_word);
            for($i = 0; $i < mysql_num_rows($sql_query); $i++){
                    $assoc_arr = mysql_fetch_assoc($sql_query);
                    $return[$i] = $assoc_arr;
            }
            if (empty($sql_query)) return 0;
            else return $return;
    }

    /*
        set_smarty_vars($varname, $var)
        It makes variable for using in smarty (in theme files)
        return No_Return;
    */
    function set_smarty_vars($varname, $var){
            global $smarty;
            $smarty->assign($varname,$var);
    }

    /*
        conv_time($type, $value)
        It returns date with given type, $value is source
        types are db2post db2rss post2db rss2db
        return String;
    */
    function conv_time($type,$value){
        if($type == "db2post"){
            $year = substr($value, 0, 4);
            $month = substr($value, 4, 2);
            $monthname = strftime("%B", strtotime("{$month}/01/{$year}"));
            $day = substr($value, 6, 2);
            $hour = substr($value, 8, 2);
            $minute = substr($value, 10, 2);
            $return_value = array("day" => $day, "month" => $month, "monthname" => $monthname, "year" => $year, "hour" => $hour, "minute" => $minute);
        }
        elseif($type == "db2rss"){
            $year = substr($value, 0, 4);
            $month = substr($value, 4, 2);
            $day = substr($value, 6, 2);
            $hour = substr($value, 8, 2);
            $minute = substr($value, 10, 2);
            $return_value = date("r", strtotime($year."-".$month."-".$day." ".$hour.":".$minute.":00"));
        }
        return $return_value;
    }

    /*
        get_something($thing, $id="", $subid="")
        if $thing = "cat", it returns entries of given $id (parent) and (if declared) $subid (child)
        if $thing = "single", it returns entry of given $id
        Also it translates licence, comments and release info
        return Array;
    */
    function get_something($thing, $id="", $subid=""){
        global $config;
        if ($thing=="single") $query="id=".$id; 
        elseif ($thing=="cat") { 
            $query="type=".$id;
            if ($subid<>"") $query.=" AND sub_type=".$subid;
        }
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}files WHERE $query AND state='1'";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $licence = get_licences($assoc_arr['license']);
            $return_array[$i] = $assoc_arr;
            $return_array[$i]['comments'] = get_comment_number($assoc_arr['id']);
            $return_array[$i]['release'] = conv_time("db2post", $assoc_arr['release']);
            $return_array[$i]['llink'] = $licence[0]['link'];
            $return_array[$i]['lname'] = $licence[0]['name'];
            $return_array[$i]['ldesc'] = $licence[0]['description'];
        }
        return $return_array;
    }

    /*
        get_comment_number($id) it returns comment number of given post $id
        return Number;
    */
    function get_comment_number($id){
        global $config;
        $sql_word = "SELECT id FROM {$config['db']['tableprefix']}comments WHERE fid='{$id}'";
        $sql_query = @mysql_query($sql_word);
        $return_string = @mysql_num_rows($sql_query);
        return $return_string;
    }

    /*
        get_licences($id=0) it returns licences
        return Array;
        if $id defined it returns String or single Array;
    */
    function get_licences($id=0){
        global $config;
        if ($id<>0) $query=" WHERE id = '{$id}'";
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}license".$query;
        return perform_sql($sql_word);
    }

    /*
        get_comments() it returns comments with nice date field
        return Array;
    */
    function get_comments($id){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}comments WHERE fid='{$id}'";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return_array[$i] = $assoc_arr;
            $return_array[$i]['date'] = conv_time("db2post", $assoc_arr['date']);
        }
        return $return_array;
    }

    /*
        get_types() it returns types with parents and childs like ['parent_type']['sub']['child_type'] sub is CONST
        return Array;
    */
    function get_types($parent=0){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}types WHERE parent_id='{$parent}'";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return_array[$i] = $assoc_arr;
            $j=0;
            if ($parent==0){
                if ($subs=get_types($return_array[$i]['id'])) {
                    foreach ( $subs as $sub_type ) {
                        $return_array[$i]['sub'][$j]=$sub_type;
                        $j++;
                    }
                }
            }
        }
        return $return_array;
    }

    function get_type($type_id){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}types WHERE id='{$type_id}'";
        return perform_sql($sql_word);
    }

    function update_user($uid="",$realname,$web,$email,$password,$add=0,$uname=""){
        global $config;
        $realname = rtag ($realname);
        $email = rtag ($email);
        $web = rtag ($web);
        $password = rtag ($password);
        if ($add) {
            $sql_word = "INSERT INTO {$config['db']['tableprefix']}users VALUES ('', '{$uname}', '{$password}','{$realname}', '{$email}', '{$web}', '3')";
        }
        else {
            $sql_word = "UPDATE {$config['db']['tableprefix']}users SET name='{$realname}', web='{$web}', email='{$email}', password='{$password}' WHERE id='$uid'";
        }
        $sql_query = @mysql_query($sql_word);
        return $sql_query;
    }

    function user_exist($uname){
        global $config;
        $sql_word = "SELECT id FROM {$config['db']['tableprefix']}users WHERE uname='$uname'";
        return perform_sql($sql_word);
    }

    function add_theme($id,$name,$type,$path,$license,$description,$note,$date) {
        global $config;
        $name = rtag($name);
        $type = rtag($type);
        $path = rtag($path);
        $license = rtag($license);
        $description = rtag($description);
        $note = rtag($note);
        $type_details = get_type($type);
        $subtype = $type;
        if ($type_details[0]["parent_id"]==0) $subtype=0; else $type=$type_details[0]["parent_id"];
        $sql_word = "INSERT INTO {$config['db']['tableprefix']}files VALUES ('', '{$type}', '{$subtype}','{$name}', '{$license}', '{$id}', '', '{$path}', '{$description}', '{$note}', '0', '0', '0', '{$date}')";
        $sql_query = @mysql_query($sql_word);
        return $sql_query;
    }

    function get_user_details($user,$pass,$state=FALSE){
        global $config;
        if (!$state) $sql_word = "SELECT * FROM {$config['db']['tableprefix']}users WHERE uname = '$user' AND password = '$pass' AND state != '3'";
        else $sql_word = "SELECT * FROM {$config['db']['tableprefix']}users WHERE id = '$user' AND uname = '$pass' AND state='0'";
        return perform_sql($sql_word);
    }

    function rtag($foo){
        return htmlspecialchars($foo,ENT_QUOTES);
    }

    function get_user_files($id){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}files WHERE user='{$id}'";
        return perform_sql($sql_word);
    }

    function set_types($type, $sub_type){
        $type = get_type($type);
        $sub_type = get_type($sub_type);

        $typem = array();
        $typem[0] = $type[0]["type"]." > ".$sub_type[0]["type"];
        $typem[1] = $type[0]["type"];
        $typem[2] = $sub_type[0]["type"];

        return $typem;
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

    function get_user_id($username){
        global $config;
        $sql_word = "SELECT id FROM {$config['db']['tableprefix']}users WHERE uname='{$username}'";
        return perform_sql($sql_word);
    }
?>