import md5
from math import *

def pass_hash(s):
  hash = md5.new(s).hexdigest()
  hash = md5.new(s + hash[2:]).hexdigest()
  return hash
  
def html_escape(s):
  s2 = s.replace('&', '&amp;')
  list = {
          '"': '&quot;',
          "'": '&apos;',
          '<': '&lt;',
          '>': '&gt;'
          }
  for f, t in list.items():
    s2 = s2.replace(f, t)
  return s2
  
def nl2br(s):
  return s.replace("\n", '<br/>')

def num2str(n):
  a = [604800, 86400, 3600, 60, 1]
  b = ['hafta', 'gün', 'saat', 'dakika', 'saniye']
  s = ''
  for i, j in zip(a, b):
    if n / i >= 1:
      s += "%d %s " % (floor(n / i), j)
      n -= i * floor(n / i)
  return s
