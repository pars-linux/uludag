ajax_addinit('init_login');

function init_login() {
  // Default values
  ajax_4u_add('grp_user');
  ajax_4o_add('grp_login');

  // Triggers
  document.getElementById('btn_login').onclick = tr_login;
  document.getElementById('lnk_logout').onclick = tr_logout;
}

