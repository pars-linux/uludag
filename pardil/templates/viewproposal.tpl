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
  #end if
</div>
#include $site_path + "templates/footer.tpl"
