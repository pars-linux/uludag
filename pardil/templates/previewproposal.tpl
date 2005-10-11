#include $site_path + "templates/header.tpl"
<div id="content">

  <h2>Bildiri - $proposal.title</h2>
  <h3>Özet</h3>
  <p>
    $proposal.summary
  </p>

  ## İçerik
  $proposal.content
</div>
#include $site_path + "templates/footer.tpl"
