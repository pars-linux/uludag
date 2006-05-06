<?php

    /*
        TUBITAK UEKAE 2005-2006
        Gökmen GÖKSEL gokmen_at_pardus.org.tr
    */

    require ('lib/modules/tools.php');
    
    build_defaults();
    build_smarty();
    ssv('DistList',get_('x','pardulDistribution')); 
    $smarty->display("homepage.html");
?>
