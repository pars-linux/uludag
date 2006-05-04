<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    function build_smarty($cf){
        global $smarty;
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

    function ssv($varname, $var){
        global $smarty;
        $smarty->assign($varname,$var);
    }

?>

