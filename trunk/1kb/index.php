<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ('lib/modules/tools.php');
    build_defaults();

    require ('lib/modules/session.php');

    build_smarty();

    ssv('DistList',get_('x','pardulDistribution'));
    session_is_registered($cf['core']["session_key"]) == TRUE ? ssv('Session',$_SESSION): ssv('Error',"Login Error");

    $smarty->display("homepage.html");

?>
