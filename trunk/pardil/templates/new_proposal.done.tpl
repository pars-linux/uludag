#include $site_path + "templates/header.tpl"
<div id="content">
  <h2>Yeni Öneri</h2>
  #if $pid and $version
    <p>Öneri eklendi.</p>
    <ul>
      <li><a href="viewproposal.py?pid=$pid&amp;version=$version">Öneriyi Görüntüle</a></li>
    </ul>
  #else
    <p>Öneri, onaylandıktan sonra yayınlanacak.</p>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
