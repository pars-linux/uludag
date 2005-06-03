window.onload = ajax_init;

var ajax_user = '';
var ajax_session = '';

var fields4users = new Array();
var fields4others = new Array();

var init_functions = new Array();

function ajax_addinit(f) {
  init_functions[init_functions.length] = f;
}

function ajax_4u_add(o) {
  fields4users[fields4users.length] = o;
}
function ajax_4o_add(o) {
  fields4others[fields4others.length] = o;
}

function ajax_init() {
  for (var i = 0; i < init_functions.length; i++) {
    eval(init_functions[i] + '()')
  }

  xhr_process('ajax_xhr/init.php', 'ajax_init', null, 'cb_ajax_init');
}

function cb_ajax_init(op, req, obj) {
  if (!req) {
    return;
  }
  if (obj != false) {
    ajax_user = obj['user'];
    ajax_session = obj['session'];
    ajax_switch_to_user();
  }
  else {
    ajax_switch_to_visitor();
  }

  document.getElementById('container').style.display = 'block';
}

function ajax_switch_to_user() {
  if (fields4users.length > 0) { 
    for (var i = 0; i < fields4users.length; i++) {
      document.getElementById(fields4users[i]).style.display = 'block';
    }
  }
  if (fields4others.length > 0) { 
    for (var i = 0; i < fields4others.length; i++) {
      document.getElementById(fields4others[i]).style.display = 'none';
    }
  }
}
function ajax_switch_to_visitor() {
  if (fields4users.length > 0) { 
    for (var i = 0; i < fields4users.length; i++) {
      document.getElementById(fields4users[i]).style.display = 'none';
    }
  }
  if (fields4others.length > 0) { 
    for (var i = 0; i < fields4others.length; i++) {
      document.getElementById(fields4others[i]).style.display = 'block';
    }
  }
}
