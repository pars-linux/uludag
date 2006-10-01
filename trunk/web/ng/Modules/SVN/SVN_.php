<?php

    #SVN Module _BEGIN_
    $SVN["Body"]="<div class='img_header'><img src='/images/texts/son_svn_degisiklikleri.gif'></div>
                    <div id='selectRepo'> 
                        <b> Depo : </b>
                            <select onChange='GetLogs(this.value,\"SVNLogs\");'> 
                                <option value='pardus'>Pardus</option>
                                <option value='uludag'>Uludağ</option>
                            </select>
                    </div>
                    <br />
                    <div id='SVNLogs'></div>";
    $SVN["Head"]  ='<script src="/Modules/SVN/SVN.js" type="text/javascript"></script>';
    $SVN["Onload"]='GetLogs("pardus","SVNLogs");';
    #SVN Module _END_

?>
