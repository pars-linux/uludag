var session = '';
var user = '';

add_init('init_login');

function init_login() {
  // Default values
  document.getElementById('grp_user').style.display = 'none';

  // Triggers
  document.getElementById('btn_login').onclick = tr_login;

  // Session control
  tr_session_control();
}

function tr_session_control() {
  var obj = new Object();
  xhr_process('ajax_xhr/session.php', 'session_control', null, "cb_session_control");
}
function cb_session_control(op, req, obj) {
  if (!req) {
    return;
  }
  if (obj != false) {
    user = obj['user'];
    session = obj['session'];
    
    var el_loginbox = document.getElementById('grp_login');
    var el_userbox = document.getElementById('grp_user');
    var el_username = document.getElementById('lbl_user_name');

    el_username.innerHTML = user;
    el_loginbox.style.display = 'none';
    el_userbox.style.display = 'block';
  }
}
