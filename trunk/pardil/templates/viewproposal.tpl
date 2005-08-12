#include $site_path + "templates/header.tpl"
<div id="content">
  #if $status == 'error':
    <p>
      Bu numaraya sahip bir öneri yok.
    </p>
  #else:
  <h2>Öneri $proposal['pid'] - $proposal['title']</h2>
  <h3>Künye</h3>
  <ul>
    <li><strong>Sürüm:</strong> $proposal['version']</li>
    <li><strong>Etiketler:</strong> <a href="?keys=pisi">PISI</a> <a href="?keys=pisi">COMAR</a> <a href="?keys=pisi">YALI</a></li>
  </ul>
  <h3>İçerik</h3>
  $proposal['content']
  <h3>Sürüm Geçmişi</h3>
  <ul>
    #for $i in $versions
      #if $i[0] == $proposal['version']
        #echo """<li>%s</li>""" % ($i[0])
      #else
        #echo """<li><a href="viewproposal.py?pid=%d&amp;version=%s">%s</a></li>""" % ($proposal['pid'], $i[0], $i[0])
      #end if
    #end for
  </ul>
  <h3>Yorumlar</h3>
  <ul>
    #for $i in $comments
      #echo """<li><b>%s</b> (<a href="#">%s</a>)<br/>%s</li>""" % ($i[2], $i[1], $i[3])
    #end for
  </ul>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
