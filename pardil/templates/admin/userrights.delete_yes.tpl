#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Erişim Hakları</h2>
    <p>
      $relid numaralı "$group - $right" erişim hakkı silindi.<br/>
    </p>
    <ul>
      <li><a href="admin_userrights.py?start=$pag_now">Listeye Dön</a></li>
    </ul>
</div>
#include $site_path + "templates/footer.tpl"
