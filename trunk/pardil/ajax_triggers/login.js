
function tr_login() {
  var obj = new Object();
  obj['user'] = document.getElementById('txt_login_user').value;
  obj['pass'] = document.getElementById('txt_login_pass').value;
  xhr_process('ajax_xhr/login.php', 'login', obj, "cb_login");
}
function cb_login(op, req, obj) {
  if (!req) {
    return;
  }

  if (obj == false) {
    session = '';
    user = '';
    alert('Girdiğiniz parola ya da kullanıcı adı yanlış.');
  }
  else if (obj['session'] != null) {
    session = obj['session'];
    user = obj['user'];

    var el_loginbox = document.getElementById('grp_login');
    var el_userbox = document.getElementById('grp_user');
    var el_username = document.getElementById('lbl_user_name');

    el_username.innerHTML = user;
    el_loginbox.style.display = 'none';
    el_userbox.style.display = 'block';
    
    alert('Kullanıcı girişi başarılı.');
  }
}
