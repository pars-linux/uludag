/*
  Copyright (c) 2005 JSON.org

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The Software shall be used for Good, not Evil.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
*/
function strpad(s, l, c) {
  var p = l - s.length;
  var ps = '';
  for (var i = 0; i < p; i++) {
    ps += c;
  }
  return ps + s;
}

function ConvertToBase(num, base) {
  var newNum = "";
  var result = num;
  var remainder = 0;
  while (result > 0) {
    result = Math.floor(num / base);
    remainder = num % base;
    num = result;

    if (remainder >= 10) {
      if (remainder == 10)
        remainder = 'A';
      if (remainder == 11)
        remainder = 'B';
      if (remainder == 12)
        remainder = 'C';
      if (remainder == 13)
        remainder = 'D';
      if (remainder == 14)
        remainder = 'E';
      if (remainder == 15)
        remainder = 'F';
    }
    newNum = "" + remainder + newNum;
  };
  return newNum;
}

  function stringify(arg, lang) {
    var c, i, l, s = '', v;
    switch (typeof arg) {
      case 'object':
        if (arg) {
          if (arg.constructor == Array) {
            for (i = 0; i < arg.length; ++i) {
              v = stringify(arg[i]);
              if (s) {
                s += ',';
              }
              s += v;
            }
            return '[' + s + ']';
          }
          else if (typeof arg.toString != 'undefined') {
            for (i in arg) {
              v = stringify(arg[i]);
              if (typeof v != 'function') {
                if (s) {
                  s += ',';
                }
                s += stringify(i) + ':' + v;
              }
            }
            return '{' + s + '}';
          }
        }
        return 'null';
      case 'number':
        return isFinite(arg) ? String(arg) : 'null';
      case 'string':
        l = arg.length;
        if (lang == 'py' || lang == 'python') {
          s = 'u"';
        }
        else if (lang == 'php'){
          s = '"';
        }
        for (i = 0; i < l; i += 1) {
          c = arg.charAt(i);
          if (c.charCodeAt() >= 32 && c.charCodeAt() <= 126) {
            if (c == '\\' || c == '"') {
              s += '\\';
            }
            s += c;
          }
          else {
            switch (c) {
              case '\b':
                s += '\\b';
                break;
              case '\f':
                s += '\\f';
                break;
              case '\n':
                s += '\\n';
                break;
              case '\r':
                s += '\\r';
                break;
              case '\t':
                s += '\\t';
                break;
              default:
                s += '\\u' + strpad(ConvertToBase(c.charCodeAt(), 16), 4, '0');
            }
          }
        }
        return s + '"';
      case 'boolean':
        return String(arg);
      default:
        return 'null';
    }
  }

  function parse(text) {
    var at = 0;
    var ch = ' ';

    function error(m) {
      throw {
        name: 'JSONError',
        message: m,
        at: at - 1,
        text: text
      };
    }

    function next() {
      ch = text.charAt(at);
      at += 1;
      return ch;
    }

    function white() {
      while (ch) {
        if (ch <= ' ') {
          next();
        }
        else if (ch == '/') {
          switch (next()) {
            case '/':
              while (next() && ch != '\n' && ch != '\r') {}
              break;
            case '*':
              next();
              for (;;) {
                if (ch) {
                  if (ch == '*') {
                    if (next() == '/') {
                      next();
                      break;
                    }
                  }
                  else {
                    next();
                  }
                }
                else {
                  error("Unterminated comment");
                }
              }
              break;
            default:
              error("Syntax error");
          }
        }
        else {
          break;
        }
      }
    }

    function string() {
      var i, s = '', t, u;
      if (ch == '"') {
        outer:
        while (next()) {
          if (ch == '"') {
            next();
            return s;
          }
          else if (ch == '\\') {
            switch (next()) {
              case 'b':
                s += '\b';
                break;
              case 'f':
                s += '\f';
                break;
              case 'n':
                s += '\n';
                break;
              case 'r':
                s += '\r';
                break;
              case 't':
                s += '\t';
                break;
              case 'u':
                u = 0;
                for (i = 0; i < 4; i += 1) {
                  t = parseInt(next(), 16);
                  if (!isFinite(t)) {
                    break outer;
                  }
                  u = u * 16 + t;
                }
                s += String.fromCharCode(u);
                break;
              default:
                s += ch;
            }
          }
          else {
            s += ch;
          }
        }
      }
      error("Bad string");
    }

    function array() {
      var a = [];
      if (ch == '[') {
        next();
        white();
        if (ch == ']') {
          next();
          return a;
        }
        while (ch) {
          a.push(value());
          white();
          if (ch == ']') {
            next();
            return a;
          }
          else if (ch != ',') {
            break;
          }
          next();
          white();
        }
      }
      error("Bad array");
    }

    function object() {
      var k, o = {};
      if (ch == '{') {
        next();
        white();
        if (ch == '}') {
          next();
          return o;
        }
        while (ch) {
          k = string();
          white();
          if (ch != ':') {
            break;
          }
          next();
          o[k] = value();
          white();
          if (ch == '}') {
            next();
            return o;
          }
          else if (ch != ',') {
            break;
          }
          next();
          white();
        }
      }
      error("Bad object");
    }

    function number() {
      var n = '', v;
      if (ch == '-') {
        n = '-';
        next();
      }
      while (ch >= '0' && ch <= '9') {
        n += ch;
        next();
      }
      if (ch == '.') {
        n += '.';
        while (next() && ch >= '0' && ch <= '9') {
          n += ch;
        }
      }
      v = +n;
      if (!isFinite(v)) {
        error("Bad number");
      }
      else {
        return v;
      }
    }

    function word() {
      switch (ch) {
        case 't':
          if (next() == 'r' && next() == 'u' && next() == 'e') {
            next();
            return true;
          }
          break;
        case 'f':
          if (next() == 'a' && next() == 'l' && next() == 's' && next() == 'e') {
            next();
            return false;
          }
          break;
        case 'n':
          if (next() == 'u' && next() == 'l' && next() == 'l') {
            next();
            return null;
          }
          break;
      }
      error("Syntax error");
    }

    function value() {
      white();
      switch (ch) {
        case '{':
         return object();
        case '[':
         return array();
        case '"':
          return string();
        case '-':
          return number();
        default:
          return ch >= '0' && ch <= '9' ? number() : word();
      }
    }
    return value();
  }
