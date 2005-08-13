import time 
def op_access(d, uid, aname):
  str_q = """SELECT Count(*)
  FROM rel_rights
    INNER JOIN rights ON rights.rid=rel_rights.rid
    INNER JOIN rel_groups ON rel_groups.gid=rel_rights.gid
    INNER JOIN users ON users.uid=rel_groups.uid
  WHERE
    users.uid=%d AND rights.keyword="%s"
  """

  return d.scalar_query(str_q % (int(uid), aname))
  
def is_maintainer(d, uid, pid):
  str_q = """SELECT Count(*)
  FROM rel_maintainers
  WHERE
    rel_maintainers.uid=%d AND rel_maintainers.pid=%d
  """

  return d.scalar_query(str_q % (int(uid), int(pid)))
