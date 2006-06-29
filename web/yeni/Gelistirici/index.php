<html>
<head>
<?php

    require_once('../utils.php');
    $Page = "Main";
    $Pardus = new Pardus($DbHost,$DbUser,$DbPass,$DbData);
    $known_pages = $Pardus->GetNiceTitles();
    foreach (array_keys($_GET) as $Parameters) {
        foreach ($known_pages as $Pvalues) {
            if ($Pvalues===$Parameters){
                $Page=$Parameters;
                break;
            }
        }
    }

    $PageContent = $Pardus->GetPage($Page,"G",False);
?>
    <title>PardusOrgTr</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="../stil.css" rel="stylesheet" type="text/css">
    <script src="../scripts/prototype.js"></script>
    <script>

        function get_news(nid) {
            var url ='utils.php';
            var linke = 'NewsID='+nid;
            var AjaxPointer = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
        }

        function showit(originalRequest){
            var newData = originalRequest.responseText;
            $('ayrintilar').innerHTML = "";
            $('ayrintilar').innerHTML = newData;
        }

        function ShowPageList(){
            var ajax = new Ajax.Updater(
                'hede',
                'http://www.pardus.org.tr',
                {
                    method:'get',
                    onComplete: showPlain
                }
            );
        }

        function showPlain(req)
        {
            $('hede').innerHTML = req.responseText;
        }
    </script>
</head>

<body onload="ShowPageList();">
<center>

<!-- Content -->
<table>
    <tr>
        <td id="header">
            <div id="menu"><b><a href="../">Ana Sayfa</a> »
            <?php
                if($Page<>"Main"){
                    echo "<a href='?'>Geliştiriciler</a> » ";
                    echo $PageContent["Title"];
                }
                else
                    echo "Geliştiriciler";
            ?>
            </b></div>
        </td>
    </tr>
    <tr>
            <td id="gelistirici" colspan=2>
            <div id="gelistiriciContent"></div>
            </td>
    </tr>
    <tr>
            <td id="mainBody" <?php if ($PageContent["PType"]==="D") { ?> style="width:770px" <?php } ?> >
                <div id="hede">
<!--                 <iframe frameborder="0" height="384px" width="100%" id="main" name="main" src="http://paketler.pardus.org.tr"></iframe> -->
                <?=$PageContent["Content"]?>
                </div>
            </td>
            <?php if ($PageContent["PType"]<>"D") { ?>
            <td id="kucular">
                <div id="hodo">
                </div>
            </td>
            <?php } ?>
    </tr>
    <tr>
        <td colspan=2 id="footer">
            Pardus TUBITAK/UEKAE 'nin Tescilli Markasıdır.
        </td>
    </tr>
 </table>

</center>
</body>
</html>
