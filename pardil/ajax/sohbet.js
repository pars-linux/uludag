window.onload = init;

var getmsg_id = -1;

function init() {
  // Tetikler
  document.getElementById('btn_msg').onclick = tr_msg;
  // Açılış işlemleri
  tr_getmsg();
}

function tr_msg() {
  var obj = document.getElementById('txt_msg').value;
  xhr_process("sohbet.py", 'msg', obj, "cb_msg");
}
function cb_msg(op, req, obj) {
  var obj = document.getElementById('txt_msg');
  obj.value = "";
}

function tr_getmsg() {
  var obj = getmsg_id + 1;
  xhr_process("sohbet.py", 'getmsg', obj, "cb_getmsg");
}
function cb_getmsg(op, req, obj) {
  var el = document.getElementById('div_msgbox');
  for (var i = 0; i < obj.length; i++) {
    el.innerHTML += '<b>' + obj[i]['ip'] +'&gt;</b> ' + obj[i]['msg'] + '<br/>';
    getmsg_id = obj[i]['id'];
    el.scrollTop += 20;
  }
  setTimeout('tr_getmsg()', 1000);
}
