function tr_login() {
  var el_user = document.getElementById('txt_login_user');
  var el_pass = document.getElementById('txt_login_pass');

  if (el_user.value == '' || el_pass.value == '') {
    alert('Kullanıcı adı ve parola boş bırakılmamalı.');
    return;
  }

  var obj = new Object();
  obj['user'] = el_user.value;
  obj['pass'] = el_pass.value;
  xhr_process('ajax_xhr/login.php', 'login', obj, 'cb_login');

  el_user.value = '';
  el_pass.value = '';
}
function cb_login(op, req, obj) {
  // TODO: Login should be announced to all modules.
  
  if (!req) {
    return;
  }

  if (obj == false) {
    ajax_session = '';
    ajax_user = '';
    alert('Girdiğiniz parola ya da kullanıcı adı yanlış.');
  }
  else if (obj['session'] != null) {
    ajax_session = obj['session'];
    ajax_user = obj['user'];
    
    ajax_switch_to_user();

    var el_username = document.getElementById('lbl_user_name');
    el_username.innerHTML = ajax_user;
    
    alert('Kullanıcı girişi başarılı.');
  }
}
function tr_logout() {
  xhr_process('ajax_xhr/logout.php', 'logout', null, 'cb_logout');
}
function cb_logout(op, req, obj) {
  // TODO: Logout should be announced to all modules.

  ajax_switch_to_visitor();
  
  var el_username = document.getElementById('lbl_user_name');
  el_username.innerHTML = '';
  
  alert('Oturum kapatıldı.');
}
