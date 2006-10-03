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
  <form action="edit_proposal.py" method="POST">
    <input type="hidden" name="action" value="edit" />
    <input type="hidden" name="pid" value="$posted['pid']"/>
    <input type="hidden" name="version" value="$posted['version']"/>
    <input type="hidden" name="p_title" value="$posted['p_title']"/>
    <input type="hidden" name="p_summary" value="$posted['p_summary']"/>
    <input type="hidden" name="p_content" value="$posted['p_content']"/>
    <input type="hidden" name="p_changelog" value="$posted['p_changelog']"/>
    <input type="hidden" name="p_version" value="$posted['p_version']"/>
    <button type="button" onclick="history.go(-1);">&laquo; Geri Git &amp; Değiştir</button>
    <button type="submit">Onayla &amp; Gönder &raquo;</button>
  </form>
</div>
#include $site_path + "templates/footer.tpl"
