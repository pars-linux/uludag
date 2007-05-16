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

    /**
     * perform_sql
     *
     * @param mixed $sql_word
     * @access public
     * @return void
     */
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
        Also it translates license, comments and release info
        return Array;
    */
    function get_something($thing="main", $id="", $subid="",$order="release",$limit="",$conv_time="db2post"){
        global $config;
        if ($thing=="single") $query="id=".$id." AND ";
        elseif ($thing=="cat") {
            $query="type=".$id." AND ";
            if ($subid<>"") $query.=" sub_type=".$subid." AND ";
        }
        elseif ($thing=="user") $query="user=".$id." AND ";
        elseif ($thing=="search") $query="name LIKE '%".$id."%' OR description LIKE '%".$id."%' AND ";
        $order = '`'.$order.'`';
        if ($limit<>"") $limitt=" LIMIT ".$limit;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Files WHERE $query state='1' ORDER by $order DESC".$limitt;
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $license = get_licenses($assoc_arr['license']);
            $return_array[$i] = $assoc_arr;
            $return_array[$i]['description'] = nl2br($assoc_arr['description']);
            $return_array[$i]['comments'] = get_comment_number($assoc_arr['id']);
            $return_array[$i]['release'] = conv_time($conv_time, $assoc_arr['release']);
            $tmp = get_user_something($return_array[$i]['user'], "UserName");
            $return_array[$i]['author'] = $tmp[0]['UserName'];
            $return_array[$i]['llink'] = $license[0]['link'];
            $return_array[$i]['lname'] = $license[0]['name'];
            $return_array[$i]['ldesc'] = $license[0]['description'];
            $temp = get_type($assoc_arr['type']);
            $return_array[$i]['ltype'] = $temp[0]['type'];
            $temp = get_type($assoc_arr['sub_type']);
            $return_array[$i]['lsubtype'] = $temp[0]['type'];
            $return_array[$i]['filetype'] = get_file_type($assoc_arr['path']);
            $return_array[$i]['filesize'] = file_exists($config['core']['path']."files/".$assoc_arr['path']) ? human_size(filesize($config['core']['path']."files/".$assoc_arr['path']),1) : "0 byte.";
            $return_array[$i]['filesize2'] = file_exists($config['core']['path']."files/".$assoc_arr['path2']) ? human_size(filesize($config['core']['path']."files/".$assoc_arr['path2']),1) : "0 byte";
        }
        return $return_array;
    }

    /*
        get_comment_number($id) it returns comment number of given post $id
        return Number;
    */
    function get_comment_number($id){
        global $config;
        $sql_word = "SELECT id FROM {$config['db']['tableprefix']}Comments WHERE fid='{$id}'";
        $sql_query = @mysql_query($sql_word);
        $return_string = @mysql_num_rows($sql_query);
        return $return_string;
    }

    /*
        get_licenses($id=0) it returns licenses
        return Array;
        if $id defined it returns String or single Array;
    */
    function get_licenses($id=0){
        global $config;
        if ($id<>0) $query=" WHERE id = '{$id}'";
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}License".$query;
        return perform_sql($sql_word);
    }

    /*
        get_comments() it returns comments with nice date field
        return Array;
    */
    function get_comments($id){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Comments WHERE fid='{$id}' ORDER by date";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return_array[$i] = $assoc_arr;
            $return_array[$i]['comment'] = nl2br($assoc_arr['comment']);
            $return_array[$i]['date'] = conv_time("db2post", $assoc_arr['date']);
            $temporary = get_user_something($assoc_arr['uid'],"UserRealName");
            $return_array[$i]['author'] = $temporary[0]['UserRealName'];
        }
        return $return_array;
    }

    /*
        get_types() it returns types with parents and childs like ['parent_type']['sub']['child_type'] sub is CONST
        return Array;
    */
    function get_types($parent=0){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Types WHERE parent_id='{$parent}'";
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
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Types WHERE id='{$type_id}'";
        return perform_sql($sql_word);
    }

    function update_user($uid="x",$realname,$web,$email,$passwordc,$uname=""){
        global $config;
        $realname       = rtag ($realname);
        $email          = rtag ($email);
        $web            = rtag ($web);
        $password       = md5(rtag($passwordc));
        if ($uname<>"") if (user_exist($uname)) return 0;
        if ($passwordc<>"") $attach_sql=", UserPass='{$password}'";
        if ($uid == "x") $sql_word = "INSERT INTO {$config['db']['users_table']} VALUES ('', '{$uname}', '{$password}','{$realname}', '{$email}', '{$web}', 'N')";
        else $sql_word = "UPDATE {$config['db']['users_table']} SET UserRealName='{$realname}', UserWeb='{$web}',UserEmail='{$email}'".$attach_sql." WHERE ID='$uid'";
        return @mysql_query($sql_word);
    }

    function user_exist($uname){
        global $config;
        $sql_word = "SELECT ID FROM {$config['db']['users_table']} WHERE UserName='$uname'";
        return perform_sql($sql_word);
    }

    function add_theme($id,$name,$type,$path,$path2,$license,$description,$note,$date,$ad_id="",$activate=0) {
        global $config;
        $name = rtag($name);
        $type = rtag($type);
        $path = rtag($path);
        $path2 = rtag($path2);
        $license = rtag($license);
        $description = rtag($description);
        $note = rtag($note);
        $type_details = get_type($type);
        $subtype = $type;
        if ($type_details[0]["parent_id"]==0) $subtype=0; else $type=$type_details[0]["parent_id"];
        if ($activate) $sql_word = "UPDATE {$config['db']['tableprefix']}Files SET name='{$name}', type='{$type}', sub_type='{$subtype}', path='{$path}', path2='{$path2}', license='{$license}', description='{$description}', supervisor='{$ad_id}', release='{$date}', state='1' WHERE id='$id'";
        else $sql_word = "INSERT INTO {$config['db']['tableprefix']}Files VALUES ('', '{$type}', '{$subtype}','{$name}', '{$license}', '{$id}', '', '{$path}', '{$path2}','{$description}', '{$note}', '0', '0', '0', '{$date}','0')";
        $sql_query = @mysql_query($sql_word);
        return $sql_query;
    }

    function get_content($content,$id,$subcontent="") {
        global $config;
        if (@fclose(@fopen( $content, "r"))) {
            $reg_content = pathinfo ($content);
            $content_path=$config['core']['path']."files/".$id."-".$reg_content['basename'];
            if (copy($content,$content_path)) {
                if (get_file_type($reg_content['basename'])=="image") {
                    $content = $config['core']['url']."3rdparty/php_thumb/phpThumb.php?src=".$config['core']['url']."files/".$id."-".$reg_content['basename']."&w=200";
                    $content_path = $config['core']['path']."files/thumbs/".$id."-".$reg_content['basename'];
                    if (copy($content,$content_path)){
                        if ($subcontent<>"") {
                            $reg_subcontent = pathinfo ($subcontent);
                            $subcontent_path=$config['core']['path']."files/2-".$id."-".$reg_subcontent['basename'];
                            if (!(copy($subcontent,$subcontent_path))) return 0;
                        }
                    return $id."-".$reg_content['basename'];
                    }
                }
                elseif (get_file_type($reg_content['basename'])=="package") {
                    if ($subcontent<>"") {
                            $reg_subcontent = pathinfo ($subcontent);
                            $subcontent_path=$config['core']['path']."files/2-".$id."-".$reg_subcontent['basename'];
                            if (!copy($subcontent,$subcontent_path)) return 0;
                    }
                return $id."-".$reg_content['basename'];
                }
            }
        }
        else return 0;
    }

    function get_file_type($file){
        $file = pathinfo ($file);
        $extension = $file["extension"];
        $package = array("zip","rar","gz","bz2","sh","tar.gz","tar.bz2","bin","pisi","skz","aiz","wav","kcsrc","mp3");
        $image   = array("gif","jpeg","jpg","png","bmp","xpm");
        foreach ($package as $key) { if ($key==$extension) return "package"; }
        foreach ($image as $key) { if ($key==$extension) return "image"; }
        return "undefined";
    }

    function get_user_details($user,$passo,$state=FALSE){
        global $config;
        $uname = $passo;
        $pass = md5($passo);
        $attach_sql =" AND UserState != '{$state}'";
        if ($user<>"") $attach_sql .=" AND ID = '{$user}'";
        if (!$state) $sql_word = "SELECT * FROM {$config['db']['users_table']} WHERE UserName = '$user' AND UserPass = '$pass' AND UserState != 'N'";
        else $sql_word = "SELECT * FROM {$config['db']['users_table']} WHERE UserName = '$uname'".$attach_sql;
        return perform_sql($sql_word);
    }

    function get_user_something($id,$thing,$opt="") {
        global $config;
        if ($opt=="UserName") $attach_sql = " UserName = '$id'"; else $attach_sql = " ID = '$id'";
        $sql_word = "SELECT $thing FROM {$config['db']['users_table']} WHERE".$attach_sql;
        return perform_sql($sql_word);
    }

    function add_comment($file_id,$user_id,$date,$comment){
        global $config;
        $comment=rtag($comment);
        $sql_word = "INSERT INTO {$config['db']['tableprefix']}Comments VALUES ('', '{$file_id}', '{$user_id}','{$date}', '{$comment}')";
        $sql_query = @mysql_query($sql_word);
        return $sql_query;
    }

    function rtag($foo){
        return htmlspecialchars($foo,ENT_QUOTES);
    }

    function get_user_files($id){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Files WHERE user='{$id}' ORDER by release DESC";
        return perform_sql($sql_word);
    }

    function get_missions($id,$rid=""){
        global $config;
        if ($rid<>"") $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Files WHERE state='0' AND id='$rid'";
        else $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Files WHERE state='0' ORDER by release DESC";
        return perform_sql($sql_word);
    }

    function set_types($type, $sub_type,$target=""){
        $type = get_type($type);
        $sub_type = get_type($sub_type);

        $typem = array();
        if ($target<>"") {
        $typem[1] = $type[0]["id"];
        $typem[2] = $sub_type[0]["id"];
        }
        else {
        $typem[0] = $type[0]["type"]." > ".$sub_type[0]["type"];
        $typem[1] = $type[0]["type"];
        $typem[2] = $sub_type[0]["type"];
        }
        return $typem;
    }

    function human_size( $bytes, $decimal = '2' ) {
        if( is_numeric( $bytes ) ) {
                $position = 0;
                $units = array( " Bytes", " KB", " MB", " GB", " TB" );
                while( $bytes >= 1024 && ( $bytes / 1024 ) >= 1 ) {
                    $bytes /= 1024;
                    $position++;
                }
            return round( $bytes, $decimal ) . $units[$position];
        }
        else {
            return "0 Byte";
        }
    }

    function sendmail($from,$to,$subject,$message,$priority){
           $mob = new Mail;
           $mob->From($from);
           $mob->To($to);
           $mob->Subject($subject);
           $mob->Body($message, "utf-8");
           $mob->Priority($priority);
           $mob->Send();
           return true;
    }

    function get_user_id($username){
        global $config;
        $sql_word = "SELECT ID FROM {$config['db']['users_table']} WHERE UserName='{$username}'";
        return perform_sql($sql_word);
    }

    function get_user($field,$value){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['users_table']} WHERE $field = '$value'";
        return perform_sql($sql_word);
    }

    function activate_user($username,$code,$action="activate"){
        global $config;
        $node = get_user("UserName",$username);
        if ($node[0]["UserState"] == "N") {
            if(md5($node[0]["ID"].$config["core"]["secretkey"]) == $code){
                if($action == "activate"){
                    $sql_word = "UPDATE {$config['db']['users_table']} SET UserState='SA' WHERE ID='{$node[0]["ID"]}' LIMIT 1";
                    if (mysql_query($sql_word)) $message["message"] = ACTIVATE_USER_OK; else $message["message"] = ACTIVATE_USER_ERROR;
                }
            }
            else {
                $message["message"]= ACTIVATE_USER_ERROR;
            }
        }
        else $message["message"] = ACTIVATED_USER;
        return $message;
    }

    function get_news($act=0) {
        global $config;
        if ($act) $attach_sql=" LIMIT 1";
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}News ".$attach_sql;
        return perform_sql($sql_word);
    }

    function get_file_something($file,$thing) {
        global $config;
        $sql_word = "SELECT $thing FROM {$config['db']['tableprefix']}Files WHERE path = '$file' OR path2 = '$file'";
        return perform_sql($sql_word);
    }

    function count_download($file) {
        global $config;
        $file_info= get_file_something($file,"id");
        $sql_word = "UPDATE {$config['db']['tableprefix']}Files SET counter=counter+1 WHERE id='{$file_info[0]["id"]}' LIMIT 1";
        return $sql_query = mysql_query($sql_word);
    }

    function get_filepaths($id){
        global $config;
        $sql_word = "SELECT path, path2 FROM {$config['db']['tableprefix']}Files WHERE id = '$id'";
        return perform_sql($sql_word);
    }

    function del_theme($id){
        global $config;
        $sql_word = "DELETE FROM {$config['db']['tableprefix']}Files WHERE id='{$id}' LIMIT 1";
        return $sql_query = mysql_query($sql_word);
    }

    function get_user_list() {
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['users_table']} WHERE UserState != 'N' ORDER BY UserName";
        return perform_sql($sql_word);
    }

    function get_file_author($fileid) {
        global $config;
        $sql_word = "SELECT user FROM {$config['db']['tableprefix']}Files WHERE id='{$fileid}'";
        $temp_sql= perform_sql($sql_word);
        $sql_word = "SELECT * FROM {$config['db']['users_table']} WHERE ID = '{$temp_sql[0]["user"]}'";
        return perform_sql($sql_word);
    }

    function pass_gen($len) {
        $pass = "" ;
        srand((float) microtime() * 10000000);
        for($i=0;$i<$len;$i++) {
            $pass.=chr(rand(33,126));
        }
        return $pass;
    }

    function SendReminderEmail($email,$uname) {
        global $config;
        $Temp = get_user_something($uname,"*","UserName");
        if ($Temp[0]["UserEmail"]==$email) {
            $uid = $Temp[0]["ID"];
            $cleanPass = pass_gen(8);
            $newPass = md5($cleanPass);
            $sql_word = "UPDATE {$config['db']['users_table']} SET UserPass='{$newPass}' WHERE ID='$uid'";
            if (@mysql_query($sql_word)) {
                $mail_message = "Siz ya da bir başkası sanat.pardus üzerinden Parola yenileme işlemi gerçekleştirdi.\n
                                 Yeni Parolanız : $cleanPass \n
                                http://sanat.pardus.org.tr adresinden giriş yapabilirsiniz.";
                if (sendmail($config['core']['email'],$email,"Parola Hatırlatma : Arto",$mail_message,"3")) return true;
            }
        }
        return 0;
    }
?>
