import MySQLdb

class mysql_db:

  def __init__(self, db_host, db_name, db_user, db_pw):
    self.conn = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pw, db=db_name)

  # 
  def query(self, str):
    c = self.conn.cursor()
    c.execute(str)
    return c.fetchall()
   
  # Satır/hücre sayısı bilinmiyorsa kullanılması önerilen fonksiyon...
  def scalar_query(self, str):
    c = self.conn.cursor()
    c.execute(str)
    return c.fetchone()[0]
    
  # Sorgu sonunda tek satır veri dönecekse, kullanılması önerilen fonksiyon...
  def row_query(self, str):
    c = self.conn.cursor()
    c.execute(str)
    return c.fetchall()[0]
    
  # Sorgudan yanıt dönmeyecekse kullanılması önerilen fonksiyon...
  def query_com(self, str):
    c = self.conn.cursor()
    c.execute(str)

  # SQL komutuna fesat karıştırılmasını önleyen fonksiyon
  def escape(self, s):
    return MySQLdb.escape_string(s)
  
  # Dict. tipindeki veriyi INSERT komutuna dönüştüren fonksiyon
  def insert(self, table, data):
    columns = []
    values = []
    for k, v in data.items():
      columns.append(k)
      values.append(""" "%s" """ % (self.escape(v)))
    queryStr = "INSERT INTO %s (%s) VALUES (%s)" % (table, ','.join(columns), ','.join(values))
    return queryStr
