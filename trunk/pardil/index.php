<?php
  require('sys.define.php');
  require('sys.database.php');

  // UGÖ No
  $int_ugo_id = (isset($_GET['id'])) ? $_GET['id'] : 1;

  // Son Revizyon:
  $str_sql = sprintf('SELECT ugo_revisions.version FROM ugo_main INNER JOIN ugo_revisions ON ugo_main.id=ugo_revisions.ugo WHERE ugo_main.id=%d ORDER BY ugo_revisions.id DESC', $int_ugo_id);
  $res_sql = mysql_query($str_sql);
  $arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  $dbl_ugo_lastrev = $arr_fetch['version'];

  // Revizyon:
  $dbl_ugo_rev = (isset($_GET['rev'])) ? $_GET['rev'] : $dbl_ugo_lastrev;
  $str_ugo_rev_date = database_query_scalar(sprintf('SELECT timestamp FROM ugo_revisions WHERE ugo=%d AND version>%f ORDER BY version DESC LIMIT 1', $int_ugo_id, $dbl_ugo_rev));

  // Önceki ve sonraki öneriler:
  $str_sql = sprintf('SELECT ugo_main.id, ugo_main.title FROM ugo_main INNER JOIN ugo_r_status ON ugo_r_status.ugo=ugo_main.id WHERE ugo_r_status.status=2 AND ugo_main.id<%d ORDER BY ugo_main.id DESC LIMIT 1', $int_ugo_id);
  $res_sql = mysql_query($str_sql);
  if (mysql_num_rows($res_sql) == 1) {
    $arr_ugo_prev = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }
  $str_sql = sprintf('SELECT ugo_main.id, ugo_main.title FROM ugo_main INNER JOIN ugo_r_status ON ugo_r_status.ugo=ugo_main.id WHERE ugo_r_status.status=2 AND ugo_main.id>%d ORDER BY ugo_main.id ASC LIMIT 1', $int_ugo_id);
  $res_sql = mysql_query($str_sql);
  if (mysql_num_rows($res_sql) == 1) {
    $arr_ugo_next = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }

  // Öneri:
  $str_time = date('Y.m.d H:i:s');
  $str_sql = sprintf('SELECT ugo_main.id, ugo_main.title, ugo_main.abstract, ugo_revisions.content, ugo_revisions.notes, ugo_revisions.version, ugo_revisions.timestamp FROM ugo_main INNER JOIN ugo_revisions ON ugo_main.id=ugo_revisions.ugo WHERE ugo_main.id=%d AND ugo_revisions.version=%f', $int_ugo_id, $dbl_ugo_rev);
  $res_sql = mysql_query($str_sql);
  $arr_ugo_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);

  // Öneri İçeriği ve İçindekiler Listesi:
  $arr_ugo_fetch['content'] = '<?xml version="1.0" encoding="utf-8"?><ugo>' . $arr_ugo_fetch['content'] . '</ugo>';
  $res_xml = simplexml_load_string($arr_ugo_fetch['content']);
  $int_ugo_content = 1;
  $arr_ugo_content = array();
  foreach ($res_xml->children() as $res_node) {
    $arr_ugo_content[] = array('no' => $int_ugo_content, 'title' => $res_node->title, 'body' => $res_node->body->asXML());
    $int_ugo_content++;
  }

  // Öneri Notları
  $arr_ugo_fetch['notes'] = '<?xml version="1.0" encoding="utf-8"?><notes>' . $arr_ugo_fetch['notes'] . '</notes>';
  $res_xml = simplexml_load_string($arr_ugo_fetch['notes']);
  $int_ugo_notes = 1;
  $arr_ugo_notes = array();
  foreach ($res_xml->children() as $res_node) {
    $arr_ugo_notes[] = array('no' => $int_ugo_notes, 'body' => $res_node->asXML());
    $int_ugo_notes++;
  }

  // Bağımlantılı Başlıklar:
  $str_sql = sprintf('SELECT ugo_main2.id, ugo_main2.title FROM ugo_main INNER JOIN ugo_r_releated ON ugo_r_releated.ugo=ugo_main.id INNER JOIN ugo_main AS ugo_main2 ON ugo_main2.id=ugo_r_releated.ugo2 WHERE ugo_main.id=%d AND ugo_r_releated.timestampB<="%s" AND ugo_r_releated.timestampE>="%s"', $int_ugo_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_list[] = sprintf('<a href="?id=%d">%s</a>', $arr_fetch['id'], $arr_fetch['title']);
  }
  $str_sql = sprintf('SELECT ugo_main.id, ugo_main.title FROM ugo_main INNER JOIN ugo_r_releated ON ugo_r_releated.ugo=ugo_main.id INNER JOIN ugo_main AS ugo_main2 ON ugo_main2.id=ugo_r_releated.ugo2 WHERE ugo_main2.id=%d AND ugo_r_releated.timestampB<="%s" AND ugo_r_releated.timestampE>="%s"', $int_ugo_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_list[] = sprintf('<a href="?id=%d">%s</a>', $arr_fetch['id'], $arr_fetch['title']);
  }
  $str_releated_list = join(', ', $arr_list);

  // Öneri Durumu:
  $str_sql = sprintf('SELECT ugo_status.name FROM ugo_main INNER JOIN ugo_r_status ON ugo_r_status.ugo=ugo_main.id INNER JOIN ugo_status ON ugo_r_status.status=ugo_status.id WHERE ugo_main.id=%d AND timestampB<="%s" AND timestampE>="%s"', $int_ugo_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  $str_ugo_status = $arr_fetch['name'];


  // Sorumlular:
  $str_sql = sprintf('SELECT name, email FROM ugo_main INNER JOIN ugo_maintainers ON ugo_maintainers.ugo=ugo_main.id INNER JOIN users ON users.id=ugo_maintainers.user WHERE ugo_main.id=%d AND ugo_maintainers.timestampB<="%s" AND ugo_maintainers.timestampE>="%s"', $int_ugo_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_maintainer_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_maintainer_list[] = $arr_fetch;
  }

  // Sürüm Geçmişi:
  $str_sql = sprintf('SELECT ugo_revisions.version, ugo_revisions.info, ugo_revisions_r_users.name AS ugo_revisor, ugo_revisions_r_users.email AS ugo_revisor_mail, ugo_revisions.timestamp FROM ugo_revisions INNER JOIN users AS ugo_revisions_r_users ON ugo_revisions_r_users.id=ugo_revisions.revisor WHERE ugo_revisions.ugo=%d ORDER BY ugo_revisions.timestamp DESC', $int_ugo_id);
  $res_sql = mysql_query($str_sql);
  $arr_revisions_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_revisions_list[] = $arr_fetch;
  }
?>
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title><?php printf('Öneri %04d - %s', $arr_ugo_fetch['id'], $arr_ugo_fetch['title']); ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
  </head>
  <body>
    <div id="container">
      <div id="header">
        <img src="images/logo2.png" alt="UGÖS"/>
      </div>
      <div id="menubar">
        <?php
          if (isset($arr_ugo_prev)) {
            printf('<a href="?id=%d" class="arrowL" title="%04d - %s">&#171</a>', $arr_ugo_prev['id'], $arr_ugo_prev['id'], $arr_ugo_prev['title']);
          }
          else {
            printf('<span class="arrowL">&#171;</span>');
          }
          if (isset($arr_ugo_next)) {
            printf('<a href="?id=%d" class="arrowR" title="%04d - %s">&#187</a>', $arr_ugo_next['id'], $arr_ugo_next['id'], $arr_ugo_next['title']);
          }
          else {
            printf('<span class="arrowR">&#187;</span>');
          }
        ?>
        <span class="title"><span><?php printf('%04d', $arr_ugo_fetch['id']); ?></span> <span><?php printf('%s', $arr_ugo_fetch['title']); ?></span></span>
      </div>
      <div id="menu">
        ...
      </div>
      <div id="content">
        <div class="ugo">
          <h1><?php printf('%s', $arr_ugo_fetch['title']); ?></h1>
          <h2>Özet</h2>
          <p><?php printf('%s', $arr_ugo_fetch['abstract']); ?></p>
          <h2>Künye</h2>
          <ul class="list-square">
            <li><b>Durum:</b> <?php printf('%s', $str_ugo_status); ?></li>
            <li><b>No:</b> <?php printf('%04d', $arr_ugo_fetch['id']); ?></li>
            <li><b>Sürüm:</b> <?php printf('%.2f', $arr_ugo_fetch['version']); ?></li>
            <li><b>Son Güncelleme:</b> <?php printf('%s', $arr_ugo_fetch['timestamp']); ?></li>
            <li><b>Bağlantılı Öneriler:</b> <?php printf('%s', ($str_releated_list) ? $str_releated_list : 'Yok'); ?></li>
          </ul>
          <h2>Sorumlular</h2>
          <ul class="list-square">
            <?php
              if (count($arr_maintainer_list) > 0) {
                foreach ($arr_maintainer_list as $arr_item) {
                  printf('<li>%s (<a href="mailto:%s">%s</a>)</li>', $arr_item['name'], $arr_item['email'], $arr_item['email']);
                }
              }
              else {
                printf('<li>Yok</li>');
              }
            ?>
          </ul>
          <div class="hr"></div>
          <h2>İçindekiler</h2>
          <ul>
            <?php
              foreach ($arr_ugo_content as $arr_item) {
                printf('<li><a href="#content%d">%s</a></li>', $arr_item['no'], $arr_item['title']);
              }
            ?>
            <li><a href="#contentNotes">Notlar</a></li>
            <li><a href="#contentRevisionHistory">Sürüm Geçmişi</a></li>
          </ul>
          <div class="hr"></div>
          <?php
            foreach ($arr_ugo_content as $arr_item) {
              printf('<h2><a name="content%d">%s</a></h2>', $arr_item['no'], $arr_item['title']);
              printf('<div>%s</div>', $arr_item['body']);
            }
          ?>
          <div class="hr"></div>
          <h2><a name="contentNotes">Notlar</a></h2>
          <dl>
          <?php
            foreach ($arr_ugo_notes as $arr_item) {
              printf('<dt><span class="no">[%d]</span> <span>%s</span></dt>', $arr_item['no'], $arr_item['body']);
            }
          ?>
          </dl>
          <div class="hr"></div>
          <h2><a name="contentRevisionHistory">Sürüm Geçmişi</a></h2>
          <div class="revisions">
            <?php
              foreach ($arr_revisions_list as $arr_item) {
                printf('<h3><a href="?id=%d&amp;rev=%0.2f">%0.2f</a></h3>', $int_ugo_id, $arr_item['version'], $arr_item['version']);
                printf('<p>%s (<a href="mailto:%s">%s</a>)</p>', $arr_item['info'], $arr_item['ugo_revisor_mail'], $arr_item['ugo_revisor']);
              }
            ?>
          </div>
        </div>
      </div>
      <div id="footer">
        &nbsp;
      </div>
    </div>
  </body>
</html>
