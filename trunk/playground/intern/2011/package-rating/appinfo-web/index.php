<?php

require_once('class.packimage.php');
require_once('class.appinfo.php');

if (!isset($_GET['p'])) {
    echo 'Appinfo server, up and running.';
    exit();
}

$p = $_GET['p'];

$appinfo = new AppInfo($p, 'appinfo.db');
if (!$appinfo->package) {
    echo 'Package name is not valid.';
    exit();
}

if (isset($_GET['s'])) {
    $s = max(1, min(5, ((float) $_GET['s'])));
    $appinfo->setScore($s);
    echo json_encode(array('p'=>$p, 'score'=>$appinfo->getScore()));
    exit();
}

$pi = new PackImage($p);

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-language" content="en" />
<link href="min/?g=css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="min/?g=js"></script>
<script type="text/javascript">
var pack = '<?php echo $p; ?>';
$(document).ready(function() {
    $('.rating').raty({
        hintList: ['', '', '', '', ''],
        half: true,
        start: <?php echo $appinfo->getScore(); ?>,
        click: function(score, evt) {
            $.getJSON('', { p: pack, s: score }, function(json) {
                $.fn.raty.start(json.score, '.rating');
                $.fn.raty.readOnly(true, '.rating');
                showMessage('success');
            });
        }
    });
});
</script>
<head>
    <title>AppInfo Server</title>
    <style>
        * {
            margin: 0;
            padding: 0;
        }

        body {
            color:white;
            font-family: 'Droid Sans', 'Dejavu Sans', Helvetica, sans-serif;
            font-size: 10pt;
        }

        .container {
            padding: 20px;
            width: 650px;
        }

        .gallery {
            height:250px;
            float: left;
            margin-right:20px;
        }
        .gallery .image {
            width: 250px;
            height:250px;
            padding: 5px;
        }

        .info {
            width: 350px;
            height:300px;
            float: right;
        }

        .info .title {
            text-shadow: 1px 1px 1px #000;
            font-size: 16pt;
            margin-bottom: 5px;
        }

        .info .summary {
            margin-bottom: 20px;
        }

        .info .description {
            margin-bottom: 20px;
        }

        .info .rating {
        }
    </style>
</head>
<body>
<div class="container">
    <div class="gallery">
        <div class="image"><?php echo ($pi->exists()) ? $pi->show() : '<img src="img/back.png">'; ?></div>
    </div>
    <div class="info">
        <div id="title" class="title"></div>
        <div id="summary" class="summary"></div>
        <div id="description" class="description"></div>
        <div class="rating"></div>
    </div>
</div>
<div class="message success">Teşekkürler!</div>
</body>
</html>
