<?php
  include(dirname(__FILE__) . '/tpl.header.php');
?>
      <div id="content">
        <div class="proposal">
          <h1><?php printf('%s', $arr_proposal['title']); ?></h1>
          <h2><?php echo __('Abstract'); ?></h2>
          <p><?php printf('%s', $arr_proposal['abstract']); ?></p>
          <h2><?php echo __('Identity'); ?></h2>
          <ul class="list-square">
            <li><b><?php echo __('Status:'); ?></b> <?php echo $str_proposal_status; ?></li>
            <li><b><?php echo __('Id:'); ?></b> <?php printf('%04d', $arr_proposal['id']); ?></li>
            <li><b><?php echo __('Version:'); ?></b> <?php printf('%.2f', $arr_proposal['version']); ?></li>
            <li><b><?php echo __('Last Update:'); ?></b> <?php printf('%s', $arr_proposal['timestamp']); ?></li>
            <li>
              <b><?php echo __('Releated Proposals:'); ?></b>
              <?php
                if (count($arr_releated) > 0) {
                  foreach ($arr_releated as $arr_item) {
                    printf('<a href="?id=%d">%s</a>', $arr_item['id'], $arr_item['title']);
                  }
                }
                else {
                  echo __('None');
                }
              ?>
            </li>
          </ul>
          <h2><?php echo __('Maintainers'); ?></h2>
          <ul class="list-square">
            <?php
              if (count($arr_maintainers) > 0) {
                foreach ($arr_maintainers as $arr_item) {
                  printf('<li>%s (<a href="mailto:%s">%s</a>)</li>', $arr_item['name'], $arr_item['email'], $arr_item['email']);
                }
              }
              else {
                printf('<li>%s</li>', __('None'));
              }
            ?>
          </ul>
          <div class="hr"></div>
          <h2><?php echo __('Contents'); ?></h2>
          <ul>
            <?php
              foreach ($arr_proposal_content as $arr_item) {
                printf('<li><a href="#content%d">%s</a></li>', $arr_item['no'], $arr_item['title']);
              }
            ?>
            <li><a href="#contentRevisionHistory"><?php echo __('Revision History'); ?></a></li>
          </ul>
          <div class="hr"></div>
          <?php
            foreach ($arr_proposal_content as $arr_item) {
              printf('<h2><a name="content%d">%s</a></h2>', $arr_item['no'], $arr_item['title']);
              printf('<div>%s</div>', $arr_item['body']);
            }
          ?>
          <br/>
          <div class="hr"></div>
          <h2><a name="contentRevisionHistory"><?php echo __('Revision History'); ?></a></h2>
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
<?php
  include(dirname(__FILE__) . '/tpl.footer.php');
?>
