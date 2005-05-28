#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import xhr

def htmlspecialchars(s):
  """
    & < > " işaretlerini HTML sayfalarında
    görüntülenebilir hale getiren fonksiyon
  """
  s = s.replace('&', '&amp;')
  l = {'<': '&lt;', '>': '&gt;', '"': '&quot;'}
  for i in l.iterkeys():
    s = s.replace(i, l[i])
  return s

def nl2br(s):
  """
    Satır sonu karakterini <br/> etiketiyle değiştiren
    fonksiyon
  """
  return s.replace("\n", "<br/>")

def msg(text):
  """
    Kullanıcıdan gelen mesajı SOHBET.LOG dosyasına kayıt
    eden fonksiyon
  """
  if len(text) == 0:
    return
  f = open('sohbet.log', 'a')
  line = os.environ['REMOTE_ADDR'] + ":" + nl2br(htmlspecialchars(text.encode('utf-8'))) + "\n"
  f.write(line)
  f.close()
  return 1

def getmsg(start_from):
  """
    Kullanıcının istediği mesajdan sonraki tüm mesajları
    kullanıcıya gönderen fonksiyon
  """
  f = open('sohbet.log', 'r')
  lines = f.readlines()
  f.close()
  msgs = []
  for linenum, line in enumerate(lines[start_from:]):
    m = line.split(':', 1)
    ip = m[0]
    msg = unicode(m[1], 'utf-8')
    msgs.append({'id': start_from+linenum,'ip': ip, 'msg': msg})
  return msgs

x = xhr.xhr()
x.register(msg)
x.register(getmsg)
x.handle()
