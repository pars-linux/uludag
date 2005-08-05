<h2>Menü</h2>
#if $session
  <p>
    Hey ${session['username']}! Sesinden tanıdım seni.
  </p>
  <p>
    <strong>Gruplar:</strong>
    #set $list = []
    #for $i, $j in $session['groups'].items()
      $list.append("""<a href="groups.py?gid=%d">%s</a>""" % (i, j))
    #end for
    #echo ', '.join($list)
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
