from Cheetah.Template import Template

def build_page(template, data={}):
  # Tema dosyasını oku
  f = open(template, 'r')
  templateStr = ''.join(f.readlines())
  f.close()
  
  # Gönderilen değişkenleri ve temayı derle...
  index = Template(templateStr, searchList=[data])

  print 'Content-Type: text/html'
  print ''
  print str(index)
