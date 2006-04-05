<?php

    /**
    *    TUBITAK UEKAE 2005-2006
    *    Gökmen GÖKSEL gokmen_at_pardus.org.tr
    *    Mawe - version 0.3
    */

    require_once 'Smarty/Smarty.class.php';
    require_once 'FCKeditor/fckeditor.php';

    /** DB FUNCTIONS BEGIN **/

    /**
    *    maWedbConnect();
    */
    function maWeDBConnect($db){
        global $db_connection;
        $db_connection = @mysql_pconnect($db['Server'], $db['UserName'], $db['Password']);
        show_mysql_errors();
        @mysql_select_db($db['DbName']);
        show_mysql_errors();
    }

    /**
    * show_mysql_errors()
    * It shows nice mysql errors
    * return NULL;
    */
    function show_mysql_errors() {
        if (mysql_error()) {
            echo "<pre>";
            echo "Database Connection Error !<br>";
            echo "Error Message : <b>".mysql_error()."</b><br>";
            echo "Error Number  : <b>".mysql_errno()."</b><br>";
            echo "</pre>";
            die();
        }
    }

    /**
    * perform_sql()
    * it performs given sql query
    * return BOOLEAN;
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

    /** DB Functions END **/

    /** SMARTY Functions BEGIN **/

    /**
    * maWeSetSmartyVar($varname, $var)
    * It makes variable for using in smarty (in theme files)
    * return NULL;
    */
    function maWeSetSmartyVar($varname, $var){
        global $maWeSmarty;
        $maWeSmarty->assign($varname,$var);
    }

	function maWeShowSmarty($page){
		global $maWeSmarty;
		$maWeSmarty->display($page);
	}
	
    function maWeSetSmarty($sm){
        global $maWeSmarty;
        $maWeSmarty = new Smarty;
        $maWeSmarty->template_dir    = $cc['Path'].'themes/'.$sm['Theme'];
        $maWeSmarty->plugins_dir     = $cc['Path'].'commonlib/php/Smarty/plugins';
        $maWeSmarty->cache_dir       = $cc['Path'].'temp';
        $maWeSmarty->caching         = $sm['Cache'];
        $maWeSmarty->compile_dir     = $cc['Path'].'temp';
        $maWeSmarty->force_compile   = $sm['Force'];
        $maWeSmarty->clear_all_cache();
       
    }
    /** SMARTY Functions END **/

    /** FCK Functions BEGIN **/

    /**
    * maWeShowFCK();
    * it shows FCK Editor with given config
    */
    function maWeShowFCK($Value=""){
        global $maWeFCK;

        $maWeFCK = new FCKeditor('maWeFCKeditor');
        $maWeFCK->BasePath = $cc['Path'].'commonlib/php/FCKeditor/';
        $maWeFCK->Height = '500px';
        $maWeFCK->Width  = '100%';
        $maWeFCK->ToolbarCanCollapse = true;

        if ($Value<>"") 
            $maWeFCK->Value = $Value;
        
        return $maWeFCK->CreateHtml();
    }
    
    /** FCK Functions END **/

    /** Misc Functions BEGIN **/

    /**
    * rtag($foo)
    * it returns removed known html tags version of $foo
    */
    function rtag($foo){
        return htmlspecialchars($foo,ENT_QUOTES);
    }

    /**
    * maWeCheckLogin($Login,$User,$Pass,$Quit)
    * huge login function, if ok return true else shows login.mt end die.
    * FIXME write Light version of it also check security
    */
	function maWeCheckLogin($Login,$User,$Pass,$Quit){
        session_start();
        if (isset($Quit)) {
            session_unregister($cc['Session']);
            header ("location: login.php");
            return;
        }
        if (session_is_registered($cc['Session'])) { 
            return true;
        }
        elseif($Login) { 
            if (maWeCheckUser($User,$Pass)){
                maWeSetSession($info,$cc['Session']);
                header ("location: login.php");
            }
            else {
                maWeSetSmartyVar("error",true);
            }
        }
        maWeShowSmarty('login.mt'); 
        die(); 
	}
	
    /**
    - maWeCheckUser($User,$Pass)
    * Checks user info from Users table
    * if ok returns user info else return false
    */
    function maWeCheckUser($User, $Pass){
        global $db;
        $Pass  = md5($Pass);
        $sql = "SELECT * FROM {$db['DbPrefix']}Users WHERE UserName = '$User' AND UserPass = '$Pass'";
        return perform_sql($sql);
    }

    function maWeSetSession($info,$key){
        @session_register($key);
        return true;
    }

    function maWeGet($Table, $Field="", $Value="") {
        global $db;
        $Field <> "" ? $Add = "WHERE $Field = '$Value'": $Add = "";
        $sql = "SELECT * FROM {$db['DbPrefix']}$Table ".$Add;
        return perform_sql($sql);
    }

    /** Misc Functions END **/

?>
