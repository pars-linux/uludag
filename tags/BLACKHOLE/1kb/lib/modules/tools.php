<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ('etc/config.php');
    require ('lib/lib.php');
    require ('lib/modules/db.php');
    require ('lib/modules/user.php');

    /**
     * build_smarty 
     * 
     * @access public
     * @return void
     */
    function build_smarty(){
        global $smarty,$cf;
        require_once($cf['core']['path'].$cf['smarty']['libdir']."/Smarty.class.php");

        $smarty = new Smarty;
        $smarty->template_dir = $cf['core']['path'].$cf['smarty']['tpldir'];
        $smarty->plugins_dir = array($cf['core']['path'].$cf['smarty']['libdir']."/plugins");
        $smarty->cache_dir = $cf['core']['path'].$cf['smarty']['cachedir'];
        $smarty->caching = $cf['smarty']['caching'];
        $smarty->compile_dir = $cf['core']['path'].$cf['smarty']['compiledir'];
        $smarty->force_compile = $cf['smarty']['forcecompile'];
        $smarty->clear_all_cache();

    }

    /**
     * ssv 
     * 
     * @param mixed $varname 
     * @param mixed $var 
     * @access public
     * @return void
     */
    function ssv($varname, $var){
        global $smarty;
        $smarty->assign($varname,$var);
    }

    /**
     * build_defaults 
     * 
     * @access public
     * @return void
     */
    function build_defaults(){
        global $cf;
        db_connection('connect', $cf['db']['host'].':'.$cf['db']['port'], $cf['db']['user'], $cf['db']['pass'], $cf['db']['dbname'], $cf['db']['ctype']);
    }

?>