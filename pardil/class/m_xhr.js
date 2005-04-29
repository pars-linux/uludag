
function xhr_php_process(x_url, x_op, x_arg, x_handler) {
  var req = new XMLHttpRequest();
  if (req) {
    req.onreadystatechange = function() {
      if (req.readyState == 4) {
        if (req.status == 200) {
          // Tamam
          var el = document.getElementById('debug');
          if (el) {
            el.innerHTML = req.responseText;
          }
          o = on_php2js(req.responseText);
          eval(x_handler + "(x_op, req, o)");
        }
        else {
          // Sunucu ile iletişimde sorun olduğunda...
        }
      }
    };
    s = on_js2php(x_arg);
    var post = 'op=' + x_op + '&arg=' + s;
    req.open('POST', x_url);
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    req.setRequestHeader('Content-Length', post.length);
    req.send(post);
  }
}

function on_php2js(s) {
  var o = new Object();
  eval("o = " + s);
  return o;
}

function on_js2php(arg) {
  var i, o, u, v;

  switch (typeof arg) {
  case 'object':
      if (arg) {
          if (arg.constructor == Array) {
              o = '';
              for (i = 0; i < arg.length; ++i) {
                  v = on_js2php(arg[i]);
                  if (o) {
                      o += ',';
                  }
                  if (v !== u) {
                      o += v;
                  } else {
                      o += 'null,';
                  }
              }
              return '[' + o + ']';
          } else if (typeof arg.toString != 'undefined') {
              o = '';
              for (i in arg) {
                  v = on_js2php(arg[i]);
                  if (v !== u) {
                      if (o) {
                          o += ',';
                      }
                      o += on_js2php(i) + ':' + v;
                  }
              }
              return '{' + o + '}';
          } else {
              return;
          }
      }
      return 'null';
  case 'unknown':
  case 'undefined':
  case 'function':
      return u;
  case 'string':
      return '"' + xhr_escape(arg) + '"';
  default:
      return String(arg);
  }
}

function xhr_escape(str_in) {
  var str_out = '';
  for (var i = 0; i < str_in.length; i++) {
    if (str_in.charCodeAt(i) == 34) {
      str_out += escape("\\\"");
    }
    else if (str_in.charCodeAt(i) == 10) {
      str_out += escape("\\n");
    }
    else if (str_in.charCodeAt(i) == 13) {
      str_out += escape("\\r");
    }
    else if ((33 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 47) || (58 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 64) || (91 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 96) || (123 <= str_in.charCodeAt(i) && str_in.charCodeAt(i) <= 127)) {
      str_out += escape(str_in.charAt(i));
    }
    else {
      str_out += str_in.charAt(i);
    }
  }
  return str_out;
}
