function xhr_process(x_url, x_op, x_arg, x_handler) {
  var req = new XMLHttpRequest();
  if (req) {
    req.onreadystatechange = function() {
      if (req.readyState == 4) {
        if (req.status == 200) {
          // ok
          var el = document.getElementById('debug');
          if (el) {
            el.innerHTML = req.responseText;
          }
          res = new String(req.responseText);
          o = py2js(res);
          eval(x_handler + "(x_op, req, o)");
        }
        else {
          // error
        }
      }
    };
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
function py2js(s) {
  if (s == '') {
    return new Object();
  }
  var esc = false;
  var qu = false;
  var dqu = false;
  var s2 = '';
  for (var i = 0; i < s.length; i++) {
    if (s.substr(i, 1) == "\\" && !esc) {
      s2 += s.substr(i, 1);
      esc = true;
    }
    else {
      if (s.substr(i, 1) == "'" && !esc && !dqu) {
        qu = !qu;
      }
      else if (s.substr(i, 1) == '"' && !esc && !qu) {
        dqu = !dqu;
      }

      if (s.substr(i, 1) == "u" && !esc && !qu && !dqu) {
        
      }
      else {
        s2 += s.substr(i, 1);
      }
      
      if (esc) {
        esc = false;
      }
    }
  }
  var o = new Object();
  eval("o = " + s2);
  return o;
}

