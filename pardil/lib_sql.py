import time 
def op_access(d, uid, aname):
  str_q = """SELECT Count(*)
  FROM rel_rights
    INNER JOIN rights ON rights.rid=rel_rights.rid
    INNER JOIN rel_groups ON rel_groups.gid=rel_rights.gid
    INNER JOIN users ON users.uid=rel_groups.uid
  WHERE
    rel_rights.timeB <= %T AND %T <= rel_rights.timeE AND
    rel_groups.timeB <= %T AND %T <= rel_groups.timeE AND
    users.uid=%d AND rights.keyword="%s"
  """.replace('%T', time.strftime('%Y-%m-%d'))

  return d.scalar_query(str_q % (int(uid), aname))
  
def is_maintainer(d, uid, pid):
  str_q = """SELECT Count(*)
  FROM rel_maintainers
  WHERE
    rel_maintainers.timeB <= %T AND %T <= rel_maintainers.timeE AND
    rel_maintainers.uid=%d AND rel_maintainers.pid=%d
  """.replace('%T', time.strftime('%Y-%m-%d'))

  return d.scalar_query(str_q % (int(uid), int(pid)))
