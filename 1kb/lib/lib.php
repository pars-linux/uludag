<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    /**
     * lib.php
     * for nowa general functions
     */

    define ( "SHOW_MYSQL_ERRORS",0);

    /**
     * db_connection
     * For General DB Conncetion to MySQ
     *
     * @param mixed $action
     * @param string $dbhost
     * @param string $dbuser
     * @param string $dbpass
     * @param string $dbname
     * @param string $dbconntype -> persistent or nonpersistent
     * @access public
     * @return void
     */
    function db_connection($action, $dbhost = "", $dbuser = "", $dbpass = "", $dbname = "", $dbconntype = ""){
        global $db_connection;

        if($action == "connect"){
            if($dbconntype == "persistent")
                $db_connection = @mysql_pconnect($dbhost, $dbuser, $dbpass);
            else
                $db_connection = @mysql_connect($dbhost, $dbuser, $dbpass);
            if(!$db_connection){
                show_mysql_errors();
                exit();
            }
            $db_select = @mysql_select_db($dbname);
            if(!$db_select){
                show_mysql_errors();
                exit();
            }
        }
        elseif($action == "disconnect")
            mysql_close($db_connection);
    }

    /**
     * show_mysql_errors
     *
     * @access public
     * @return void
     */
    function show_mysql_errors() {
        echo "<pre>";
        echo "Database Connection Error !<br>";
        echo "Error Message : <b>".mysql_error()."</b><br>";
        echo "Error Number  : <b>".mysql_errno()."</b><br>";
        echo "</pre>";
    }

    /**
     * perform_sql
     * Performs SQL of given Word and returns the result as array
     *
     * @param mixed $sql_word
     * @access public
     * @return array
     */
    function perform_sql($sql_word){

        $sql_query = mysql_query($sql_word);
        if (SHOW_MYSQL_ERRORS) show_mysql_errors( );

        for($i = 0; $i < mysql_num_rows($sql_query); $i++){
            $assoc_arr = mysql_fetch_assoc($sql_query);
            $return[$i] = $assoc_arr;
        }
        if (empty($sql_query)) return 0;
        else return $return;
    }

    /**
     * rtag
     * Returns removed known html tags of foo
     *
     * @param mixed $foo
     * @access public
     * @return string
     */
    function rtag($foo){
        return htmlspecialchars($foo,ENT_QUOTES);
    }


    /**
     * conv_time
     * Convert value for db2post or db2rssls
     *
     * @param mixed $type
     * @param mixed $value
     * @access public
     * @return string
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
        elseif($type == "db2archive"){
            $year = substr($value, 0, 4);
            $month = substr($value, 4, 2);
            $return_value = strftime("%B", strtotime("{$month}/01/{$year}"))."&nbsp;".$year;
        }
        return $return_value;
    }

?>
