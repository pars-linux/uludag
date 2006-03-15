
//  TUBITAK UEKAE 2005-2006
//  Gökmen GÖKSEL gokmen_at_pardus.org.tr

var mikExp = /[$\\@\\\#%\^\&\*\(\)\[\]\+\_\{\}\`\~\ \|\"\!\'\?]/;

function dodacheck(val) {
    var strPass = val.value;
    var strLength = strPass.length;
    var lchar = val.value.charAt((strLength) - 1);
    if(lchar.search(mikExp) != -1) {
    var tst = val.value.substring(0, (strLength) - 1);
    val.value = tst;
   }
}

/* form field lar için düzenle .. */

function doanothercheck(form) {
    if (frm.username.value.length < 3)              { alert('Kullanıcı Adı en az 4 (dört) karakterden oluşmalıdır !'); frm.username.select(); frm.username.focus(); return false;}
    if (frm.realname.value.length < 6)              { alert('Ad Soyad boş ya da eksik !');return false;}
    if (frm.email.value.length < 8)                 { alert('E-Mail boş ya da eksik !');return false;}
    if (frm.password.value.length <= 4)             { alert('Parola boş ya da eksik (en az 5 karakter)!');return false;}
    if (frm.password.value !== frm.password_.value) { alert('Parola ve Parola Tekrar birbirini tutmuyor !'); return false;}
    return true;
}


function tV(el, src) {
    var v = el.style.display == "block";
    var str = src.innerHTML;
    el.style.display = v ? "none" : "block";
    src.innerHTML = v ? str.replace(/up/, "down") : str.replace(/down/, "up");
}

function init () {
    $('p_vendor').onkeyup = function () {
        get_vendorlist();
    }
    $('p_vendor').onblur = function () {
     var dropmenu = new Element.ClassNames('dropmen');
    dropmenu.set("dropmenu");
    }
   
}

function get_vendorlist() {
    var linke='vendorpref='+$('p_vendor').value;
    var url ='check.php';
    var myAjax = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
}

function showit(originalRequest){
    var newData = originalRequest.responseText;
    var dropmenu = new Element.ClassNames('dropmen');
    dropmenu.set("droppedmenu");
    $('p_vendor_list').innerHTML = newData;
}
