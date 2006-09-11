<?php

    #SVN Module _BEGIN_
    $SVN["Body"]="<img src='images/newdesign/head-svn-degisiklik.png'>
                    <div id='selectRepo'> 
                        <b> Depo : </b>
                            <select onChange='GetLogs(this.value,\"SVNLogs\");'> 
                                <option value='pardus'>Pardus</option>
                                <option value='uludag'>Uludağ</option>
                            </select>
                    </div>
                    <div id='SVNLogs'></div>";
    $SVN["Head"]  ='<script src="Modules/SVN/SVN.js"></script>';
    $SVN["Onload"]='GetLogs("pardus","SVNLogs");';
    #SVN Module _END_

?>
