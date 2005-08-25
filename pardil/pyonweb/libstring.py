import md5

def pass_hash(s):
  hash = md5.new(s).hexdigest()
  hash = md5.new(s + hash[2:]).hexdigest()
  return hash
  
def html_escape(s):
  s2 = s.replace('&', '&amp;')
  list = {'"': '&quot;', "'": '&apos;', '<': '&lt;', '>': '&gt;'}
  for f, t in list.items():
    s2 = s2.replace(f, t)
  return s2
  
def nl2br(s):
  return s.replace("\n", '<br/>')
