<h2>Menü</h2>
#if $session
  <p>
    Hey ${session['username']}! Sesinden tanıdım seni.
  </p>
  <ul>
    <li><a href="logout.py">Çıkış</a></li>
  </ul>
  #else
  <ul>
    <li><a href="login.py">Kullanıcı Girişi</a></li>
    <li><a href="register.py">Kayıt</a></li>
  </ul>
#end if
  <ul>
    <li><a href="proposals.py">Öneriler</a></li>
    <li><a href="new_proposal.py">Öneri Ekle</a></li>
  </ul>
  Gereksiz kullananlar cezalandırılacak!
  <ul>
    <li><a href="new_proposal.py?pid=1&amp;version=1.0.0">Öneri # 1 - Sürüm 1.0.0</a></li>
    <li><a href="new_proposal.py?pid=1&amp;version=1.1.0">Öneri # 1 - Sürüm 1.1.0</a></li>
    <li><a href="new_proposal.py?pid=1">Öneri # 1 - Son Sürüm</a></li>
  </ul>
