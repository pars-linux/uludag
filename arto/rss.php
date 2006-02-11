<?php
ob_start();

echo "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\"?>";
include_once("globals.php");

$posts = get_something("","","","release","10","db2rss");

// set content-type to xml
Header("Content-type: text/xml; charset=utf-8");
?>
<!-- generator="Arto Feed Engine/Arto v<?=$config['arto']['version']?>" -->
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
    <title><?=$config['core']['title']?></title>
    <link><?=$config['core']['url']?></link>
    <description><?=$config['core']['desc']?></description>
    <pubDate><?php echo date("r"); ?></pubDate>
    <generator>http://arto.fasafiso.org/?version=<?=$config['arto']['version']?></generator>
    <?php for($i = 0; $i < count($posts); $i++){ ?>
    <item>
        <title><?=$posts[$i]['name']?></title>
        <link><?=$config['core']['url']?>?id=<?=$posts[$i]['id']?></link>
        <comments><?=$config['core']['url']?>?id=<?=$posts[$i]['id']?>#comments</comments>
        <pubDate><?=$posts[$i]['release']?></pubDate>
        <dc:creator><?=$posts[$i]['author']?></dc:creator>
        <guid isPermaLink="true"><?=$config['core']['url']?>?id=<?=$posts[$i]['id']?></guid>
        <description><?=htmlspecialchars(strip_tags($posts[$i]['description']), ENT_QUOTES)?></description>
        <content:encoded><?=htmlspecialchars($posts[$i]['description'], ENT_QUOTES)?></content:encoded>
    </item>
    <?php } ?>
</channel>
</rss>
<?
ob_end_flush();
?>
