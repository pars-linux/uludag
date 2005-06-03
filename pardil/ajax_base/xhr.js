function xhr_process(x_url, x_op, x_arg, x_handler) {
  var req = new XMLHttpRequest();
  if (req) {
    req.onreadystatechange = function() {
      if (req.readyState == 4) {
        var el_notify = document.getElementById('notifier');
        if (el_notify) {
          el_notify.style.visibility = 'hidden';
        }
        if (req.status == 200) {
          // ok
          var el = document.getElementById('debug');
          if (el) {
            el.innerHTML = req.responseText;
          }
          res = new String(req.responseText);
          o = json2obj(res);
          eval(x_handler + "(x_op, req, o)");
        }
        else {
          // error
          alert('İşlem sırasında, sunucu ile iletişim problemi yaşandı.\n\nDaha sonra tekrar deneyin.');
          eval(x_handler + "(x_op, null, null)");
        }
      }
    };
    var el_notify = document.getElementById('notifier');
    if (el_notify) {
      el_notify.style.visibility = 'visible';
    }
    s = stringify(x_arg);
    var post = 'op=' + xescape(x_op) + '&arg=' + xescape(s) + '&';
    req.open('POST', x_url);
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    req.send(post);
  }
}
function xescape(s) {
  s = encodeURI(s);
  s =  s.replace(/&/g, '%26');
  s =  s.replace(/;/g, '%3B');
  s =  s.replace(/\+/g, '%2B');
  return s;
}
function json2obj(s) {
  if (s == '') {
    return new Object();
  }
  var o = new Object();
  eval("o = " + s);
  return o;
}

