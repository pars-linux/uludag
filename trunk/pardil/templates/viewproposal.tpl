#include $site_path + "templates/header.tpl"
<div id="content">
  #def printError($s)
    #if $errors.has_key($s)
      #echo """<div class="error_msg">%s</div>""" % ($errors[$s])
    #end if
  #end def

  #def printValue($s, $t='')
    #if not $errors.has_key($s) and $posted.has_key($s)
      #echo $posted[$s]
    #else
      #echo $t
    #end if
  #end def

  <h2>Öneri $proposal.pid - $proposal.title</h2>
  <h3>Künye</h3>
  <ul>
    <li><strong>Sürüm:</strong> $proposal.version</li>
    <li><strong>Sorumlular:</strong>
      #set $list = []
      #for $i in $maintainers
        $list.append("""<a href="#">%s</a>""" % $i.user)
      #end for
      #echo ', '.join($list)
    </li>
  </ul>
  #if $is_maintainer
  <h3>Yönetim</h3>
  <ul>
    <li><a href="edit_proposal.py?pid=$proposal.pid&amp;version=$proposal.version">Yeni Sürüm</a></li>
  </ul>
  #end if
  <h3>Özet</h3>
  <p>
    $proposal.summary
  </p>
  <h3>Amaç</h3>
  $proposal.purpose
  <p>&nbsp;</p>
  <h3>Detaylar</h3>
  $proposal.content
  <p>&nbsp;</p>
  <h3>Çözüm</h3>
  $proposal.solution
  <p>&nbsp;</p>
  <h3>Sürüm Geçmişi</h3>
  <ul>
    #for $i in $versions
      #if $i == $proposal.version
        #echo """<li>%s</li>""" % ($i)
      #else
        #echo """<li><a href="viewproposal.py?pid=%d&amp;version=%s">%s</a></li>""" % ($proposal.pid, $i, $i)
      #end if
    #end for
  </ul>
  <h3>Yorumlar</h3>
    #if len($comments)
      <ul>
      #for $i in $comments
        #echo """<li><div class="r1"><a href="#">%s</a>:</div><div class="r2">%s</div</li>""" % ($i['user'], $i['comment'])
      #end for
     </ul>
    #else
      <p>
        Önerinin bu sürümüne hiç yorum yapılmamış.
      </p>
    #end if
  #if $may_comment
  <form action="viewproposal.py" method="post">
    <input type="hidden" name="pid" value="$proposal.pid" />
    <input type="hidden" name="version" value="$proposal.version" />
    <fieldset>
      <legend>Yorum</legend>
      <div class="required">
        <textarea class="widetext" id="p_comment" name="p_comment" cols="60" rows="5"></textarea>
        #echo $printError('p_comment')
      </div>
    </fieldset>
    <fieldset>
      <button type="submit" name="action" value="comment">Gönder</button>
    </fieldset>
  </form>
  #end if
</div>
#include $site_path + "templates/footer.tpl"
