<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr">
  <head>
    <title><?php printf(_('Proposal %04d - %s'), $arr_proposal['id'], $arr_proposal['title']); ?></title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" href="style.css" type="text/css" />
    <link rel="icon" type="image/png" href="favicon.png">
  </head>
  <body>
    <div id="container">
      <div id="header">
        <img src="images/logo2.png" alt="Pardil"/>
      </div>
      <div id="menubar">
        <?php
          if (isset($arr_proposal_prev)) {
            printf('<a href="?id=%d" class="arrowL" title="%04d - %s">&#171</a>', $arr_proposal_prev['id'], $arr_proposal_prev['id'], $arr_proposal_prev['title']);
          }
          else {
            printf('<span class="arrowL">&#171;</span>');
          }
          if (isset($arr_proposal_next)) {
            printf('<a href="?id=%d" class="arrowR" title="%04d - %s">&#187</a>', $arr_proposal_next['id'], $arr_proposal_next['id'], $arr_proposal_next['title']);
          }
          else {
            printf('<span class="arrowR">&#187;</span>');
          }
        ?>
        <span class="title"><span><?php printf('%04d', $arr_proposal['id']); ?></span> <span><?php printf('%s', $arr_proposal['title']); ?></span></span>
      </div>
      <div id="content">
        <div class="proposal">
          <h1><?php printf('%s', $arr_proposal['title']); ?></h1>
          <h2><?php echo _('Abstract'); ?></h2>
          <p><?php printf('%s', $arr_proposal['abstract']); ?></p>
          <h2><?php echo _('Identity'); ?></h2>
          <ul class="list-square">
            <li><b><?php echo _('Status:'); ?></b> <?php printf('%s', _($str_proposal_status)); ?></li>
            <li><b><?php echo _('Id:'); ?></b> <?php printf('%04d', $arr_proposal['id']); ?></li>
            <li><b><?php echo _('Version:'); ?></b> <?php printf('%.2f', $arr_proposal['version']); ?></li>
            <li><b><?php echo _('Last Update:'); ?></b> <?php printf('%s', $arr_proposal['timestamp']); ?></li>
            <li>
              <b><?php echo _('Releated Proposals:'); ?></b>
              <?php
                if (count($arr_releated) > 0) {
                  foreach ($arr_releated as $arr_item) {
                    printf('<a href="?id=%d">%s</a>', $arr_item['id'], $arr_item['title']);
                  }
                }
                else {
                  echo _('None');
                }
              ?>
            </li>
          </ul>
          <h2><?php echo _('Maintainers'); ?></h2>
          <ul class="list-square">
            <?php
              if (count($arr_maintainers) > 0) {
                foreach ($arr_maintainers as $arr_item) {
                  printf('<li>%s (<a href="mailto:%s">%s</a>)</li>', $arr_item['name'], $arr_item['email'], $arr_item['email']);
                }
              }
              else {
                printf('<li>%s</li>', _('None'));
              }
            ?>
          </ul>
          <div class="hr"></div>
          <h2><?php echo _('Contents'); ?></h2>
          <ul>
            <?php
              foreach ($arr_proposal_content as $arr_item) {
                printf('<li><a href="#content%d">%s</a></li>', $arr_item['no'], $arr_item['title']);
              }
            ?>
            <li><a href="#contentNotes"><?php echo _('Notes'); ?></a></li>
            <li><a href="#contentRevisionHistory"><?php echo _('Revision History'); ?></a></li>
          </ul>
          <div class="hr"></div>
          <?php
            foreach ($arr_proposal_content as $arr_item) {
              printf('<h2><a name="content%d">%s</a></h2>', $arr_item['no'], $arr_item['title']);
              printf('<div>%s</div>', $arr_item['body']);
            }
          ?>
          <div class="hr"></div>
          <h2><a name="contentNotes"><?php echo _('Notes'); ?></a></h2>
          <dl>
          <?php
            foreach ($arr_notes as $arr_item) {
              printf('<dt><span class="no">[%d]</span> <span>%s</span></dt>', $arr_item['no'], $arr_item['body']);
            }
          ?>
          </dl>
          <div class="hr"></div>
          <h2><a name="contentRevisionHistory"><?php echo _('Revision History'); ?></a></h2>
          <div class="revisions">
            <?php
              foreach ($arr_revisions as $arr_item) {
                printf('<h3><a href="?id=%d&amp;rev=%0.2f">%0.2f</a></h3>', $arr_proposal['id'], $arr_item['version'], $arr_item['version']);
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
