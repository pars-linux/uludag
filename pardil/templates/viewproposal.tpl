#include $site_path + "templates/header.tpl"
<div id="content">
  #if $status == 'error':
    <p>
      Bu numaraya sahip bir öneri yok.
    </p>
  #else:
  <h2>Öneri $proposal['pid'] - $proposal['title']</h2>
  <ul>
    <li><strong>Sürüm:</strong> $proposal['version']</li>
  </ul>
  $proposal['content']
  <h3>Sürüm Geçmişi</h3>
  <ul>
    #for $i in $versions
      #if $i[0] == $proposal['version']
        #echo """<li><b>%s</b></li>""" % ($i[0])
      #else
        #echo """<li><a href="viewproposal.py?pid=%d&amp;version=%s">%s</a></li>""" % ($proposal['pid'], $i[0], $i[0])
      #end if
    #end for
  </ul>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
