<?php
  require('sys.define.php');
  require('sys.database.php');

  // Öneri No
  $int_pardil_id = (isset($_GET['id'])) ? $_GET['id'] : 1;

  // Son Revizyon:
  $str_sql = sprintf('SELECT pardil_revisions.version FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d ORDER BY pardil_revisions.id DESC', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  $arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  $dbl_pardil_lastrev = $arr_fetch['version'];

  // Revizyon:
  $dbl_pardil_rev = (isset($_GET['rev'])) ? $_GET['rev'] : $dbl_pardil_lastrev;
  $str_pardil_rev_date = database_query_scalar(sprintf('SELECT timestamp FROM pardil_revisions WHERE proposal=%d AND version>%f ORDER BY version DESC LIMIT 1', $int_pardil_id, $dbl_pardil_rev));

  // Önceki ve sonraki öneriler:
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main INNER JOIN pardil_r_status ON pardil_r_status.proposal=pardil_main.id WHERE pardil_r_status.status=2 AND pardil_main.id<%d ORDER BY pardil_main.id DESC LIMIT 1', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  if (mysql_num_rows($res_sql) == 1) {
    $arr_pardil_prev = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main INNER JOIN pardil_r_status ON pardil_r_status.proposal=pardil_main.id WHERE pardil_r_status.status=2 AND pardil_main.id>%d ORDER BY pardil_main.id ASC LIMIT 1', $int_pardil_id);
  $res_sql = mysql_query($str_sql);
  if (mysql_num_rows($res_sql) == 1) {
    $arr_pardil_next = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  }

  // Öneri:
  $str_time = date('Y.m.d H:i:s');
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title, pardil_main.abstract, pardil_revisions.content, pardil_revisions.notes, pardil_revisions.version, pardil_revisions.timestamp FROM pardil_main INNER JOIN pardil_revisions ON pardil_main.id=pardil_revisions.proposal WHERE pardil_main.id=%d AND pardil_revisions.version=%f', $int_pardil_id, $dbl_pardil_rev);
  $res_sql = mysql_query($str_sql);
  $arr_pardil_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);

  // Öneri İçeriği ve İçindekiler Listesi:
  $arr_pardil_fetch['content'] = '<?xml version="1.0" encoding="utf-8"?><pardil>' . $arr_pardil_fetch['content'] . '</pardil>';
  $res_xml = simplexml_load_string($arr_pardil_fetch['content']);
  $int_pardil_content = 1;
  $arr_pardil_content = array();
  foreach ($res_xml->children() as $res_node) {
    $arr_pardil_content[] = array('no' => $int_pardil_content, 'title' => $res_node->title, 'body' => $res_node->body->asXML());
    $int_pardil_content++;
  }

  // Öneri Notları
  $arr_pardil_fetch['notes'] = '<?xml version="1.0" encoding="utf-8"?><notes>' . $arr_pardil_fetch['notes'] . '</notes>';
  $res_xml = simplexml_load_string($arr_pardil_fetch['notes']);
  $int_pardil_notes = 1;
  $arr_pardil_notes = array();
  foreach ($res_xml->children() as $res_node) {
    $arr_pardil_notes[] = array('no' => $int_pardil_notes, 'body' => $res_node->asXML());
    $int_pardil_notes++;
  }

  // Bağımlantılı Başlıklar:
  $str_sql = sprintf('SELECT pardil_main2.id, pardil_main2.title FROM pardil_main INNER JOIN pardil_r_releated ON pardil_r_releated.proposal=pardil_main.id INNER JOIN pardil_main AS pardil_main2 ON pardil_main2.id=pardil_r_releated.proposal2 WHERE pardil_main.id=%d AND pardil_r_releated.timestampB<="%s" AND pardil_r_releated.timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_list[] = sprintf('<a href="?id=%d">%s</a>', $arr_fetch['id'], $arr_fetch['title']);
  }
  $str_sql = sprintf('SELECT pardil_main.id, pardil_main.title FROM pardil_main INNER JOIN pardil_r_releated ON pardil_r_releated.proposal=pardil_main.id INNER JOIN pardil_main AS pardil_main2 ON pardil_main2.id=pardil_r_releated.proposal2 WHERE pardil_main2.id=%d AND pardil_r_releated.timestampB<="%s" AND pardil_r_releated.timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_list[] = sprintf('<a href="?id=%d">%s</a>', $arr_fetch['id'], $arr_fetch['title']);
  }
  $str_releated_list = join(', ', $arr_list);

  // Öneri Durumu:
  $str_sql = sprintf('SELECT pardil_status.name FROM pardil_main INNER JOIN pardil_r_status ON pardil_r_status.proposal=pardil_main.id INNER JOIN pardil_status ON pardil_r_status.status=pardil_status.id WHERE pardil_main.id=%d AND timestampB<="%s" AND timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC);
  $str_pardil_status = $arr_fetch['name'];


  // Sorumlular:
  $str_sql = sprintf('SELECT name, email FROM pardil_main INNER JOIN pardil_maintainers ON pardil_maintainers.proposal=pardil_main.id INNER JOIN users ON users.id=pardil_maintainers.user WHERE pardil_main.id=%d AND pardil_maintainers.timestampB<="%s" AND pardil_maintainers.timestampE>="%s"', $int_pardil_id, $str_time, $str_time);
  $res_sql = mysql_query($str_sql);
  $arr_maintainer_list = array();
  while ($arr_fetch = mysql_fetch_array($res_sql, MYSQL_ASSOC)) {
    $arr_maintainer_list[] = $arr_fetch;
  }

  // Sürüm Geçmişi:
  $str_sql = sprintf('SELECT pardil_revisions.version, pardil_revisions.info, pardil_revisions_r_users.name AS pardil_revisor, pardil_revisions_r_users.email AS pardil_revisor_mail, pardil_revisions.timestamp FROM pardil_revisions INNER JOIN users AS pardil_revisions_r_users ON pardil_revisions_r_users.id=pardil_revisions.revisor WHERE pardil_revisions.proposal=%d ORDER BY pardil_revisions.timestamp DESC', $int_pardil_id);
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
    <title><?php printf('Öneri %04d - %s', $arr_pardil_fetch['id'], $arr_pardil_fetch['title']); ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
  </head>
  <body>
    <div id="container">
      <div id="header">
        <img src="images/logo2.png" alt="pardilS"/>
      </div>
      <div id="menubar">
        <?php
          if (isset($arr_pardil_prev)) {
            printf('<a href="?id=%d" class="arrowL" title="%04d - %s">&#171</a>', $arr_pardil_prev['id'], $arr_pardil_prev['id'], $arr_pardil_prev['title']);
          }
          else {
            printf('<span class="arrowL">&#171;</span>');
          }
          if (isset($arr_pardil_next)) {
            printf('<a href="?id=%d" class="arrowR" title="%04d - %s">&#187</a>', $arr_pardil_next['id'], $arr_pardil_next['id'], $arr_pardil_next['title']);
          }
          else {
            printf('<span class="arrowR">&#187;</span>');
          }
        ?>
        <span class="title"><span><?php printf('%04d', $arr_pardil_fetch['id']); ?></span> <span><?php printf('%s', $arr_pardil_fetch['title']); ?></span></span>
      </div>
      <div id="menu">
        ...
      </div>
      <div id="content">
        <div class="proposal">
          <h1><?php printf('%s', $arr_pardil_fetch['title']); ?></h1>
          <h2>Özet</h2>
          <p><?php printf('%s', $arr_pardil_fetch['abstract']); ?></p>
          <h2>Künye</h2>
          <ul class="list-square">
            <li><b>Durum:</b> <?php printf('%s', $str_pardil_status); ?></li>
            <li><b>No:</b> <?php printf('%04d', $arr_pardil_fetch['id']); ?></li>
            <li><b>Sürüm:</b> <?php printf('%.2f', $arr_pardil_fetch['version']); ?></li>
            <li><b>Son Güncelleme:</b> <?php printf('%s', $arr_pardil_fetch['timestamp']); ?></li>
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
              foreach ($arr_pardil_content as $arr_item) {
                printf('<li><a href="#content%d">%s</a></li>', $arr_item['no'], $arr_item['title']);
              }
            ?>
            <li><a href="#contentNotes">Notlar</a></li>
            <li><a href="#contentRevisionHistory">Sürüm Geçmişi</a></li>
          </ul>
          <div class="hr"></div>
          <?php
            foreach ($arr_pardil_content as $arr_item) {
              printf('<h2><a name="content%d">%s</a></h2>', $arr_item['no'], $arr_item['title']);
              printf('<div>%s</div>', $arr_item['body']);
            }
          ?>
          <div class="hr"></div>
          <h2><a name="contentNotes">Notlar</a></h2>
          <dl>
          <?php
            foreach ($arr_pardil_notes as $arr_item) {
              printf('<dt><span class="no">[%d]</span> <span>%s</span></dt>', $arr_item['no'], $arr_item['body']);
            }
          ?>
          </dl>
          <div class="hr"></div>
          <h2><a name="contentRevisionHistory">Sürüm Geçmişi</a></h2>
          <div class="revisions">
            <?php
              foreach ($arr_revisions_list as $arr_item) {
                printf('<h3><a href="?id=%d&amp;rev=%0.2f">%0.2f</a></h3>', $int_pardil_id, $arr_item['version'], $arr_item['version']);
                printf('<p>%s (<a href="mailto:%s">%s</a>)</p>', $arr_item['info'], $arr_item['pardil_revisor_mail'], $arr_item['pardil_revisor']);
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
