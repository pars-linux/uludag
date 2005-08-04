        <h2>Menü</h2>
        <p>
          Yazı. <a href="1.html">Köprü</a>. <a href="2.html">Diğer köprü</a>.
        </p>
        #if $session
        <p>
          Sen ${session['username']}'sin, tanıdım sesinden!
        </p>
        #end if
