import string
import types

##    json.py implements a JSON (http://json.org) reader and writer.
##    Copyright (C) 2005  Patrick D. Logan
##    Contact mailto:patrickdlogan@stardecisions.com
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Lesser General Public
##    License as published by the Free Software Foundation; either
##    version 2.1 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Lesser General Public License for more details.
##
##    You should have received a copy of the GNU Lesser General Public
##    License along with this library; if not, write to the Free Software
##    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


class _StringGenerator:
	def __init__(self, string):
		self.string = string
		self.index = -1
	def peek(self):
		i = self.index + 1
		if i < len(self.string):
			return self.string[i]
		else:
			return None
	def next(self):
		self.index = self.index + 1
		if self.index < len(self.string):
			return self.string[self.index]
		else:
			raise StopIteration
	def all(self):
		return self.string

class WriteException(Exception):
    pass

class ReadException(Exception):
    pass

class JsonReader:
    def read(self, s):
        self._generator = _StringGenerator(s)
        result = self._read()
        return result

    def _read(self):
        self._eatWhitespace()
        peek = self._peek()
        if peek == '{':
            return self._readObject()
        elif peek == '[':
            return self._readArray()            
        elif peek == '"':
            return self._readString()
        elif peek == '-' or peek.isdigit():
            return self._readNumber()
        elif peek == 't':
            return self._readTrue()
        elif peek == 'f':
            return self._readFalse()
        elif peek == 'n':
            return self._readNull()
        elif peek == '/':
            self._readComment()
            return self._read()
        else:
            raise ReadException, "Input is not valid JSON: '%s'" % self._generator.all()

    def _readTrue(self):
        self._assertNext('t', "true")
        self._assertNext('r', "true")
        self._assertNext('u', "true")
        self._assertNext('e', "true")
        return True

    def _readFalse(self):
        self._assertNext('f', "false")
        self._assertNext('a', "false")
        self._assertNext('l', "false")
        self._assertNext('s', "false")
        self._assertNext('e', "false")
        return False

    def _readNull(self):
        self._assertNext('n', "null")
        self._assertNext('u', "null")
        self._assertNext('l', "null")
        self._assertNext('l', "null")
        return None

    def _assertNext(self, ch, target):
        if self._next() != ch:
            raise ReadException, "Trying to read %s: '%s'" % (target, self._generator.all())

    def _readNumber(self):
        isfloat = False
        result = self._next()
        peek = self._peek()
        while peek is not None and (peek.isdigit() or peek == "."):
            isfloat = isfloat or peek == "."
            result = result + self._next()
            peek = self._peek()
        try:
            if isfloat:
                return float(result)
            else:
                return int(result)
        except ValueError:
            raise ReadException, "Not a valid JSON number: '%s'" % result

    def _readString(self):
        result = ""
        assert self._next() == '"'
        try:
            while self._peek() != '"':
                ch = self._next()
                if ch == "\\":
                    ch = self._next()
                    if ch == "b":
                        ch = "\b"
                    elif ch == "f":
                        ch = "\f"
                    elif ch == "n":
                        ch = "\n"
                    elif ch == "r":
                        ch = "\r"
                    elif ch == "t":
                        ch = "\t"
                    elif ch == "u":
		        ch4096 = self._next()
			ch256  = self._next()
			ch16   = self._next()
			ch1    = self._next()
			n = 4096    * self._hexDigitToInt(ch4096)
			n = n + 256 * self._hexDigitToInt(ch256)
			n = n + 16  * self._hexDigitToInt(ch16)
			n = n + self._hexDigitToInt(ch1)
			ch = unichr(n)
                    elif ch not in '"/\\':
                        raise ReadException, "Not a valid escaped JSON character: '%s' in %s" % (ch, self._generator.all())
                result = result + ch
        except StopIteration:
            raise ReadException, "Not a valid JSON string: '%s'" % self._generator.all()
        assert self._next() == '"'
        return result

    def _hexDigitToInt(self, ch):
        try:
            result = {
		    'a': 10,
		    'A': 10,
		    'b': 11,
		    'B': 11,
		    'c': 12,
		    'C': 12,
		    'd': 13,
		    'D': 13,
		    'e': 14,
		    'E': 14,
		    'f': 15,
		    'F': 15
		}[ch]
	except KeyError:
	    try:
	        result = int(ch)
	    except ValueError:
	         raise ReadException, "The character %s is not a hex digit." % ch
        return result

    def _readComment(self):
        assert self._next() == "/"
        second = self._next()
        if second == "/":
            self._readDoubleSolidusComment()
        elif second == '*':
            self._readCStyleComment()
        else:
            raise ReadException, "Not a valid JSON comment: %s" % self._generator.all()

    def _readCStyleComment(self):
        try:
            done = False
            while not done:
                ch = self._next()
                done = (ch == "*" and self._peek() == "/")
                if not done and ch == "/" and self._peek() == "*":
                    raise ReadException, "Not a valid JSON comment: %s, '/*' cannot be embedded in the comment." % self._generator.all()
            self._next()
        except StopIteration:
            raise ReadException, "Not a valid JSON comment: %s, expected */" % self._generator.all()

    def _readDoubleSolidusComment(self):
        try:
            ch = self._next()
            while ch != "\r" and ch != "\n":
                ch = self._next()
        except StopIteration:
            pass

    def _readArray(self):
        result = []
        assert self._next() == '['
        done = self._peek() == ']'
        while not done:
            item = self._read()
            result.append(item)
            self._eatWhitespace()
            done = self._peek() == ']'
            if not done:
                ch = self._next()
                if ch != ",":
                    raise ReadException, "Not a valid JSON array: '%s' due to: '%s'" % (self._generator.all(), ch)
        return result

    def _readObject(self):
        result = {}
        assert self._next() == '{'
        done = self._peek() == '}'
        while not done:
            key = self._read()
            if type(key) is not types.StringType:
                raise ReadException, "Not a valid JSON object key (should be a string): %s" % key
            self._eatWhitespace()
            ch = self._next()
            if ch != ":":
                raise ReadException, "Not a valid JSON object: '%s' due to: '%s'" % (self._generator.all(), ch)
            self._eatWhitespace()
            val = self._read()
            result[key] = val
            self._eatWhitespace()
            done = self._peek() == '}'
            if done:
                self._next()
            else:
                ch = self._next()
                if ch != ",":
                    raise ReadException, "Not a valid JSON object: '%s' due to: '%s'" % (self._generator.all(), ch)
        return result

    def _eatWhitespace(self):
        while self._peek() in string.whitespace:
            self._next()

    def _peek(self):
        return self._generator.peek()

    def _next(self):
        return self._generator.next()

class JsonWriter:
    def write(self, obj):
        self._result = ""
        return self._write(obj)

    def _write(self, obj):
        ty = type(obj)
        if ty is types.DictType:
            n = len(obj)
            self._append("{")
            for k, v in obj.items():
                self._write(k)
                self._append(":")
                self._write(v)
                n = n - 1
                if n > 0:
                    self._append(",")
            self._append("}")
        elif ty is types.ListType:
            n = len(obj)
            self._append("[")
            for item in obj:
                self._write(item)
                n = n - 1
                if n > 0:
                    self._append(",")
            self._append("]")
        # Begin hack
        elif ty is types.StringType:
            self._append(repr(obj))
        elif ty is types.UnicodeType:
            self._append(repr(obj)[1:])
        # End hack
        elif ty is types.IntType:
            self._append(str(obj))
        elif ty is types.FloatType:
            self._append("%f" % obj)
        elif obj is True:
            self._append("true")
        elif obj is False:
            self._append("false")
        elif obj is None:
            self._append("null")
        else:
            raise WriteException, "Cannot write in JSON: %s" % obj
        return self._result

    def _append(self, s):
        self._result = self._result + s

def write(obj):
    return JsonWriter().write(obj)

def read(s):
    return JsonReader().read(s)
