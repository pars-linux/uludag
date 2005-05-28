#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import xhr

kullanicilar = {u'Bahadır': u'Linüks'}

def giris(o):
  if kullanicilar.get_key(o['isim']) == o['sifre']:
    return 'e'
  return 'h'

x = xhr.xhr()
x.register(giris)
x.handle()
