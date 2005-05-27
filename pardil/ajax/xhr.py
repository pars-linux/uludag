# -- coding: utf-8 --
import cgi
import sys

class xhr:
  """
    XHR sınıfı, ilgili sayfaya "POST" edilen anahtar kelime,
    çalıştırılmasına izin verilen fonksiyonlar arasında ise,
    fonksiyonu çalıştıranve çıktısını kullanıcıya gönderen bir
    sınıftır.
  """
  fn_py = {}
  
  def register(self, py):
    """İzin verilen fonksiyonları listeye ekleyen fonksiyon"""
    self.fn_py[py.func_name] = py

  def handle(self):
    """
      "op" argümanında belirtilen fonksiyon listedeyse,
      fonksiyonu çağır ve çıktısını gönder.
    """
    print "Content-type: text/html; charset=utf-8"
    print
    form = cgi.FieldStorage()
    if form.has_key('op') and self.fn_py.has_key(form["op"].value):
      arg = eval(form['arg'].value)
      print repr(self.fn_py[form["op"].value](arg))
    sys.exit()
