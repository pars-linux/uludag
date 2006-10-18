
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

function tV(el, src) {
    var v = el.style.display == "block";
    var str = src.innerHTML;
    el.style.display = v ? "none" : "block";
    src.innerHTML = v ? str.replace(/up/, "down") : str.replace(/down/, "up");
}

function init () {
    $('username').onblur = function () {
    checkuser();
    }
}

function checkuser() {
    var linke='username='+$('username').value;
    var url ='check.php';
    var myAjax = new Ajax.Request(url,{method:'get', parameters: linke, onComplete: showit});
}

function showit(originalRequest){
    var newData = originalRequest.responseText;
    $('result').innerHTML = newData;
}
