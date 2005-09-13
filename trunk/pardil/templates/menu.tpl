<div class="box">
  <h2>Kullanıcı Menüsü</h2>
#if $session
  <ul>
    <li><a href="#">${session['username']}</a></li>
    <li><a href="login.py?action=logout">Çıkış</a></li>
  </ul>
  #else
  <ul>
    <li><a href="login.py">Kullanıcı Girişi</a></li>
    <li><a href="register.py">Kayıt</a></li>
  </ul>
#end if
</div>
<div class="box">
  <h2>Öneriler</h2>
  <ul>
    <li><a href="proposals.py">Öneriler</a></li>
    #if 'proposals_add' in $acl
    <li><a href="new_proposal.py">Öneri Ekle</a></li>
    #end if
  </ul>
</div>
