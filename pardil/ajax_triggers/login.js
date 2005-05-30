var session = '';
var user = '';

function tr_login() {
  var obj = new Object();
  obj['user'] = document.getElementById('txt_login_user').value;
  obj['pass'] = document.getElementById('txt_login_pass').value;
  xhr_process('ajax_xhr/login.php', 'login', obj, "cb_login", "php");
}
function cb_login(op, req, obj) {
  if (obj == 'h') {
    session = '';
    user = '';
    alert('Hatalı parola ya da kullanıcı adı.');
    window.status = '';
  }
  else if (obj['session'] != null) {
    session = obj['session'];
    user = obj['user'];
    alert('Kullanıcı girişi başarılı.\nHoşgeldin ' + user + '!');
    window.status = 'Kullanıcı: ' + obj['user'];
  }
}
