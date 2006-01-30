# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import MySQLdb

class mysql:

  def __init__(self, db_host, db_name, db_user, db_pw):
    self.conn = MySQLdb.connect(
                                host=db_host,
                                user=db_user,
                                passwd=db_pw,
                                db=db_name
                                )

  # Sorgula...
  def query(self, str, par=()):
    c = self.conn.cursor()
    c.execute(str, par)
    return c.fetchall()
   
  # Satır/hücre sayısı bilinmiyorsa kullanılması önerilen fonksiyon...
  def scalar_query(self, str, par=()):
    c = self.conn.cursor()
    c.execute(str, par)
    try:
      return c.fetchone()[0]
    except:
      return
    
  # Sorgu sonunda tek satır veri dönecekse, kullanılması önerilen fonksiyon...
  def row_query(self, str, par=()):
    c = self.conn.cursor()
    c.execute(str, par)
    try:
      return c.fetchone()
    except:
      return
    
  # Sorgudan yanıt dönmeyecekse kullanılması önerilen fonksiyon...
  def query_com(self, str, par=()):
    c = self.conn.cursor()
    c.execute(str, par)

  # SQL komutuna fesat karıştırılmasını önleyen fonksiyon
  def escape(self, s):
    return MySQLdb.escape_string(s)
  
  # Dict. tipindeki veriyi INSERT komutuna dönüştüren fonksiyon
  # Sorguyu biz oluşturduğumuz için, % operatörü ile sokuşturma yapıyoruz.
  def insert(self, table, data):
    columns = []
    values = []
    for k, v in data.items():
      columns.append(k)
      values.append(""" "%s" """ % (self.escape(str(v))))
    q = """INSERT INTO %s (%s)
           VALUES (%s)""" % (table, ','.join(columns), ','.join(values))
    
    self.query_com(q)
    return self.scalar_query('SELECT LAST_INSERT_ID()')
