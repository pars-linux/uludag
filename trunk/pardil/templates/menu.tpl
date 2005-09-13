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
#if 'administrate' in $acl or $site_admin
<div class="box">
  <h2>Yönetim</h2>
  <ul>
    #if 'administrate_groups' in $acl or $site_admin
    <li><a href="admin_groups.py">Gruplar</a></li>
    #end if
    #if 'administrate_rights' in $acl or $site_admin
    <li><a href="admin_rights.py">Erişim Kodları</a></li>
    #end if
    #if 'administrate_usergroups' in $acl or $site_admin
    <li><a href="admin_usergroups.py">Kullanıcı Grupları</a></li>
    #end if
    #if 'administrate_userrights' in $acl or $site_admin
    <li><a href="admin_userrights.py">Grup Hakları</a></li>
    #end if
    #if 'administrate_maintainers' in $acl or $site_admin
    <li><a href="admin_maintainers.py">Öneri Sorumluları</a></li>
    #end if
    #if 'administrate_pending' in $acl or $site_admin
    <li><a href="admin_p_proposals.py">Bekleyen Öneriler</a></li>
    #end if
    #if 'administrate_comments' in $acl or $site_admin
    <li><a href="admin_comments.py">Yorumlar</a></li>
    #end if
  </ul>
</div>
#end if
