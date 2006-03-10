<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require_once ("functions.php");

    /*
        make_*($parameters) it adds or updates a field with given paramaeters
        return Boolean;
    */
    function make_category($categoryid="x",$categoryname,$parentid=0){
        global $config;
        $categoryname = rtag($categoryname);
	$categoryid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Categories VALUES ('','{$categoryname}', '{$parentid}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Categories SET CategoryName='{$categoryname}', ParentID='{$parentid}' WHERE ID='$categoryid'";
        return mysql_query($sql_word);
    }

    function make_distribution($distid="x",$distversion,$distname="Pardus"){
        global $config;
        $distversion = rtag($distversion);
        $distname = rtag($distname);
	$distid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Distribution VALUES ('','{$distversion}', '{$distname}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Distribution SET DistVersion='{$distversion}', DistName='{$distname}' WHERE ID='$distid'";
        return @mysql_query($sql_word);
    }

    function make_user($uid="x",$realname,$web,$email,$passwordc,$uname=""){
        global $config;
        $realname = rtag ($realname);
        $email = rtag ($email);
        $web = rtag ($web);
        $password = md5(rtag($passwordc));
        if ($passwordc<>"") $attach_sql=", UserPass='{$password}'";
        $uid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Users VALUES ('', '{$uname}', '{$password}','{$realname}', '{$email}', '{$web}', 'G', '')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Users SET UserName='{$realname}', UserWeb='{$web}', UserEmail='{$email}'".$attach_sql." WHERE ID='$uid'";
        return @mysql_query($sql_word);
    }

    function make_vendor($vendorid="x",$vendorname,$vendorurl,$vendorvid=''){
        global $config;
        $vendorname = rtag ($vendorname);
        $vendorurl = rtag ($vendorurl);
        $vendorvid = rtag ($vendorvid);
        $vendorid = "x" ? $sql_word = "INSERT INTO {$config['db']['tableprefix']}Vendors VALUES ('', '{$vendorname}', '{$vendorurl}','{$vendorvid}')" :
        $sql_word = "UPDATE {$config['db']['tableprefix']}Vendors SET VendorName'{$vendorname}', VendorURL='{$vendorurl}', VendorID='{$vendorvid}' WHERE ID='$vendorid'";
        return @mysql_query($sql_word);
    }

    /*
        get_categories() it returns types with parents and childs like ['parent_type']['sub']['child_type'] sub is CONST
        return Array;
    */
    function get_categories($parent=0){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}Categories WHERE parentID='{$parent}'";
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

    /*
        get_($id) it returns a field from $table which has $id
        $table can be Categories,Distribution,Hardwares,Users,Platform,Vendors,Comments or ActionCompatibility
        return Array;
    */
    function get_($id,$table){
        global $config;
        $sql_word = "SELECT * FROM {$config['db']['tableprefix']}{$table} WHERE ID='{$id}'";
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

?>
