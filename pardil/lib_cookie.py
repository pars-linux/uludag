import os
import Cookie

# FIXME:
# En kısa zamanda Cookie sınıfı değiştirilecek...

class cookie:
  def __init__(self):
    self.c = Cookie.Cookie()
    try:
      cr = os.environ['HTTP_COOKIE']
    except KeyError:
      pass
    else:
      self.c.load(cr)

  def get(self, k, e=''):
    if self.c.has_key(k):
      return self.c[k].value
    return e
    
  def set(self, k, v='', l=1800):
    self.c[k] = v
    self.c[k]['max-age'] = l

  def save(self):
    print self.c
