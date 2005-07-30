from Cheetah.Template import Template

def build_page(template, data):
  f = open(template, 'r')
  templateStr = ''.join(f.readlines())
  f.close()
  index = Template(templateStr, searchList=[data])
  return str(index)
