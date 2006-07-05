<html>
<head>

<?php
    
    $ActivePage = "M";
    require_once('utils.php');
    require_once('Modules/Main.php');
    require_once('Modules/RSS.php');

    $Blogs = new RssRead($BlogRssLink);

?>

    <title><?=$PageTitle?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="stil.css" rel="stylesheet" type="text/css">
    <script src="scripts/prototype.js"></script>
    <script src="scripts/scriptaculous.js"></script>
    <script src="scripts/effects.js"></script>
    <script>

        function get_news(nid) {
            var url ='utils.php';
            var linke = 'NewsID='+nid;
            var AjaxPointer = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
        }

        function showit(originalRequest){
            var newData = originalRequest.responseText;
            $('haber').innerHTML = "";
            $('haber').innerHTML = newData;
            new Effect.Highlight('haber',{startcolor:'#CCE0E6', endcolor:'#FFFFFF'});
            $('haber').style.background = "#FFF";
        }
    </script>
</head>

<body>
<center>
<table>

<?php 
    if($Page==="Main") 
        include ('index-data.php');
    else 
        include ('child-data.php');
?>
    
    <tr>
        <td colspan=2>
            <div id="footer-forpw">Pardus TUBITAK/UEKAE 'nin Tescilli Markasıdır.</div>
        </td>
    </tr>
 </table>

</center>
</body>
</html>
