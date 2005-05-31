var session = '';
var user = '';

function tr_login_php() {
  var obj = new Object();
  obj['user'] = document.getElementById('txt_login_user').value;
  obj['pass'] = document.getElementById('txt_login_pass').value;
  xhr_process('ajax_xhr/login.php', 'login', obj, "cb_login", "php");
}
function tr_login_py() {
  var obj = new Object();
  obj['user'] = document.getElementById('txt_login_user').value;
  obj['pass'] = document.getElementById('txt_login_pass').value;
  xhr_process('ajax_xhr/login.py', 'login', obj, "cb_login", "php");
}
function cb_login(op, req, obj) {
  if (obj == 'h') {
    session = '';
    user = '';
    alert('Girdiğiniz parola ya da kullanıcı adı yanlış.\n\nAncak AJAX bileşeninin tıkır tıkır çalıştığı kesin :)');
    window.status = '';
  }
  else if (obj['session'] != null) {
    session = obj['session'];
    user = obj['user'];
    alert('Kullanıcı girişi başarılı.\n\nVe evet, AJAX bileşeni çalışıyor :)');
    window.status = 'Kullanıcı: ' + obj['user'];
  }
}
