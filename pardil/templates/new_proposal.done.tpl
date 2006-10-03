#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yeni Bildiri</h2>
  #if $pid and $version
    <p>Bildiri eklendi.</p>
    <ul>
      <li><a href="viewproposal.py?pid=$pid&amp;version=$version">Bildiriyi Görüntüle</a></li>
    </ul>
  #else
    <p>Bildiri, onaylandıktan sonra yayınlanacak.</p>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
