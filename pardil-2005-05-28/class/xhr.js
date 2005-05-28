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
          o = on_php2js(req.responseText);
          eval(x_handler + "(x_op, req, o)");
        }
        else {
          // error
        }
      }
    };
    s = JSON.stringify(x_arg);
    var post = 'op=' + xescape(x_op) + '&arg=' + xescape(s);
    req.open('POST', x_url);
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    req.setRequestHeader('Content-Length', post.length);
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
function on_php2js(s) {
  var o = new Object();
  eval("o = " + s);
  return o;
}

