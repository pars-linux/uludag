#!/usr/bin/python

import cgi

def index():
  form = cgi.FieldStorage()

  print 'Content-Type: text/html'
  print ''
  print form.getvalue('tag')

index()
