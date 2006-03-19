<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require_once ("functions.php");

    /*
        make_*($parameters) it adds or updates a field with given parameters
        return Boolean;
    */
    function make_hardware($hwid="x",$productname,$vendor,$deviceid,$bustype,$categoryid,$date,$status=0,$userid,$suserid="",$state,$todo){
        global $config;

        $productname    = rtag(strtolower($productname));
        $vendor         = rtag(strtoupper($vendor));
        $deviceid       = rtag($deviceid);
        $bustype        = rtag($bustype);
        $categoryid     = rtag($categoryid);
        $adddate        = rtag($adddate);
        $date           = rtag($date);
        $status         = rtag($status);
        $userid         = rtag($userid);
        $suserid        = rtag($suserid);
        $todo           = rtag($todo);

        $hwid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Hardwares VALUES ('','{$productname}','{$vendor}','{$deviceid}','{$bustype}','{$categoryid}','{$date}','','{$status}','{$userid}','{$suserid}','{$todo}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Hardwares SET HWProductName='{$productname}', HWVendor='{$vendor}',HWDeviceID='{$deviceid}',HWBusType='{$bustype}',HWCategoryID='{$categoryid}',HWUpdateDate='{$date}',Status='{$status}',UserID='{$userid}',SuperUserID='{$suserid}', ToDo = '{$todo}' WHERE ID='$hwid'";
        if (mysql_query($sql_word)) if (make_hardware_status(mysql_insert_id(),$state)) return TRUE; else return FALSE;
    }

    function make_hardware_status($hwid,$state){
        global $config;
        $sql_word = "DELETE FROM {$config['db']['tableprefix']}ActionCompatibility WHERE HWID='{$hwid}'";
        $sql_query = @mysql_query($sql_word);
        foreach ($state as $key => $value){
            $sql_word = "INSERT INTO {$config['db']['tableprefix']}ActionCompatibility VALUES ('','{$key}','0','{$hwid}','{$value}')";
            mysql_query($sql_word);
        }
        return TRUE;
    }

    function make_category($categoryid="x",$categoryname,$parentid=0){
        global $config;
        $categoryname   = rtag($categoryname);
        $categoryid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Categories VALUES ('','{$categoryname}', '{$parentid}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Categories SET CategoryName='{$categoryname}', ParentID='{$parentid}' WHERE ID='$categoryid'";
        return mysql_query($sql_word);
    }

    function make_distribution($distid="x",$distversion,$distname="Pardus"){
        global $config;
        $distversion    = rtag($distversion);
        $distname       = rtag($distname);
        $distid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Distribution VALUES ('','{$distversion}', '{$distname}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Distribution SET DistVersion='{$distversion}', DistName='{$distname}' WHERE ID='$distid'";
        return @mysql_query($sql_word);
    }

    function make_platform($platformid="x",$platform){
        global $config;
        $platform       = rtag($platform);
        $platformid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Platform VALUES ('','{$platform}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Platform SET Platform='{$platform}' WHERE ID='$platformid'";
        return @mysql_query($sql_word);
    }

    function make_user($uid="x",$realname,$web,$email,$passwordc,$uname=""){
        global $config;
        $realname       = rtag ($realname);
        $email          = rtag ($email);
        $web            = rtag ($web);
        $password       = md5(rtag($passwordc));
        if ($uname<>"") if (user_exist($uname)) return 0;
        if ($passwordc<>"") $attach_sql=", UserPass='{$password}'";
        $uid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Users VALUES ('', '{$uname}', '{$password}','{$realname}', '{$email}', '{$web}', 'N')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Users SET UserRealName='{$realname}', UserWeb='{$web}', UserEmail='{$email}'".$attach_sql." WHERE ID='$uid'";
        return @mysql_query($sql_word);
    }

    function make_vendor($act="x",$vendorname){
        global $config;
        $vendorname     = rtag ($vendorname);
        $act = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Vendors VALUES ('{$vendorname}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Vendors SET VendorName='{$vendorname}' WHERE VendorName='{$vendorname}'";
        return @mysql_query($sql_word);
    }

    function make_comment($commentid="x",$hwid,$uid,$comment,$adddate){
        global $config;
        $hwid           = rtag ($hwid);
        $uid            = rtag ($uid);
        $comment        = rtag ($comment);
        $commentid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Comments VALUES ('', '{$hwid}','{$uid}','{$comment}','{$adddate}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Comments SET HWID'{$hwid}', UID='{$uid}', Comment='{$comment}', AddDate='{$adddate}' WHERE ID='$commentid'";
        return @mysql_query($sql_word);
    }

    /*
        get_categories() it returns types with parents and childs like ['parent_type']['sub']['child_type'] sub is CONST
        return Array;
    */
    function get_categories($parent=0){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Categories WHERE ParentID='{$parent}'";
        $sql_query = @mysql_query($sql_word);
        for($i = 0; $i < @mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return_array[$i] = $assoc_arr;
            $j=0;
            if ($parent==0){
                if ($subs=get_categories($return_array[$i]['ID'])) {
                    foreach ( $subs as $sub_type ) {
                        $return_array[$i]['sub'][$j]=$sub_type;
                        $j++;
                    }
                }
            }
        }
        return $return_array;
    }

    /*
        get_($id) it returns a field from $table which has $id
        $table can be Categories,Distribution,Hardwares,Users,Platform,Vendors,Comments or ActionCompatibility
        return Array;
    */
    function get_($id="x",$table){
        global $config;
        $id = "x" ? $sql_word = "SELECT * FROM {$config['db']['tableprefix']}{$table}" : $sql_word = "SELECT * FROM {$config['db']['tableprefix']}{$table} WHERE ID='{$id}'";
        return perform_sql($sql_word);
    }

    /*
        del_($id,$table) it removes a field from $table which has $id
        $table can be Categories,Distribution,Hardwares,Users,Platform,Vendors,Comments or ActionCompatibility
        return Boolean;
    */
    function del_($id,$table){
        global $config;
	$sql_word = "DELETE FROM {$config['db']['tableprefix']}{$table} WHERE ID='{$id}'";
        return @mysql_query($sql_word);
    }

    /*
        user_exist($uname)
        it checks the user $uname and returns users info
        return Array;
    */
    function user_exist($uname){
        global $config;
        $sql_word = "SELECT ID FROM {$config['db']['tableprefix']}Users WHERE UserName='$uname'";
        return perform_sql($sql_word);
    }

    /*
        mail_exist($email)
        it checks the user $email and returns users info
        return Array;
    */
    function mail_exist($email){
        global $config;
        $sql_word = "SELECT ID FROM {$config['db']['tableprefix']}Users WHERE UserEmail='$email'";
        return perform_sql($sql_word);
    }

    function get_user_details($user,$pass,$state="x"){
        global $config;
        $passx  = md5($pass);
        $state = "x" ? $attach_sql =" AND UserState != 'N'" : $attach_sql =" AND UserState = '{$state}'";
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Users WHERE UserName = '$user' AND UserPass = '$passx'".$attach_sql;
        return perform_sql($sql_word);
    }

    function find_vendor($pref) {
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Vendors WHERE VendorName LIKE '$pref%'";
        return perform_sql($sql_word);
    }

    function find_product($vendor,$name,$category,$deviceid,$bustype) {
        global $config;

        $name   =       rtag(strtolower($name));
        $vendor =       rtag(strtoupper($vendor));

        if ($category   <>  "all_categories") $attach_sql .= " AND HWCategoryID = '$category' ";
        if ($vendor     <>  "") $attach_sql .= " AND HWVendor = '$vendor' ";
        if ($deviceid   <>  "") $attach_sql .= " AND HWDeviceID = '$deviceid' ";
        if ($bustype    <>  "") $attach_sql .= " AND HWBusType = '$bustype' ";
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Hardwares WHERE HWProductName LIKE '%$name%'".$attach_sql." AND Status=1";
        return perform_sql($sql_word);
    }

    function get_products($field,$userid){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Hardwares WHERE $field = '$userid'";
        return perform_sql($sql_word);
    }


?>
