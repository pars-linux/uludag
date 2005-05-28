window.onload = init;

function init() {
  // Tetikler
  document.getElementById('btn_giris').onclick = tr_giris;
}

function tr_giris() {
  var obj = new Object();

  obj['isim'] = document.getElementById('txt_isim').value;
  obj['sifre'] = document.getElementById('txt_sifre').value;

  xhr_process("giris.py", 'giris', obj, "cb_giris");
}
function cb_giris(op, req, obj) {
  if (obj == 'e') {
    document.getElementById('grp_giris').style.display = 'none';
    document.getElementById('grp_kullanici').style.display = 'block';
  }
  else {
    alert('Hatalı kullanıcı adı ya da şifre.');
  }
}
