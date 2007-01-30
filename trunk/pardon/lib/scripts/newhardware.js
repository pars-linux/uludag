
//  TUBITAK UEKAE 2005-2006
//  Gökmen GÖKSEL gokmen_at_pardus.org.tr

function doanothercheck(form) {
    if (frm.p_vendor.value.length < 2)              { alert('Üretici kısmı boş bırakılamaz !'); frm.p_vendor.select(); frm.p_vendor.focus(); return false;}
    if (frm.p_name.value.length < 3)                { alert('Ürün Adı boş bırakılamaz !');return false;}
    return true;
}

function tV(el, src) {
    var v = el.style.display == "block";
    var str = src.innerHTML;
    el.style.display = v ? "none" : "block";
    src.innerHTML = v ? str.replace(/up/, "down") : str.replace(/down/, "up");
}

timer = 0;

function init () {
    $('p_vendor').onkeyup = function () {
        get_vendorlist();
    }

    $('p_vendor').onblur = function () {
    timer = setTimeout('bilmemne()', 1000);
    }
    $('p_vendor').onmouseover = function () {
     timer = clearTimeout(timer);
    }
    $('dropmen').onmouseout = function () {
     timer = setTimeout('bilmemne()', 1000);
    }
}

function bilmemne() {
    var dropmenu = new Element.ClassNames('dropmen');
    dropmenu.set('dropmenu');
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
