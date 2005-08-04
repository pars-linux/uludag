import md5

def pass_hash(s):
  hash = md5.new(s).hexdigest()
  hash = md5.new(s + hash[2:]).hexdigest()
  return hash
