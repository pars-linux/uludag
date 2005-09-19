#include $site_path + "templates/header.tpl"
<div id="content">
  #for $i in $news
    <div class="news">
      <div class="logo"><img src="$i.icon" alt="" /></div>
      <div class="content">
        <h2>$i.title</h2>
        <p>
          <strong>Gönderen:</strong> <a href="#">$i.user</a>
        </p>
        $i.content
      </div>
    </div>
  #end for
</div>
#include $site_path + "templates/footer.tpl"
