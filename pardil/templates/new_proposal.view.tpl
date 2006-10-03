#include $site_path + "templates/header.tpl"
<div id="content">

  <h2>Bildiri - $proposal.title</h2>
  <h3>Özet</h3>
  <p>
    $proposal.summary
  </p>

  ## İçerik
  $proposal.content

  <div class="seperator"></div>
  <form action="new_proposal.py" method="POST">
    <input type="hidden" name="action" value="new" />
    #if 'p_pid' in $posted:
    <input type="hidden" name="p_pid" value="$posted['p_pid']"/>
    #end if
    <input type="hidden" name="p_title" value="$posted['p_title']"/>
    <input type="hidden" name="p_summary" value="$posted['p_summary']"/>
    <input type="hidden" name="p_content" value="$posted['p_content']"/>
    <button type="button" onclick="history.go(-1);">&laquo; Geri Git &amp; Değiştir</button>
    <button type="submit">Onayla &amp; Gönder &raquo;</button>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
