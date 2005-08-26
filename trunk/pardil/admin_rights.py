#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_index'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('administrate'):
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

def index():
  p['rights'] = []
  list = p.db.query('SELECT rid, category, keyword, label FROM rights ORDER BY rid ASC')
  for i in list:
    p['rights'].append({'rid': i[0], 'category': i[1], 'keyword': i[2], 'label': i[3]})

  p.template = site_config['path'] + 'templates/admin/rights.tpl'

def delete():
  try:
    p['rid'] = int(p.form['delete'])
  except:
    p.template = site_config['path'] + 'templates/admin/rights.error.tpl'
  else:
    p['label'] = p.db.scalar_query('SELECT label FROM rights WHERE rid=%d' % (p['rid']))
    if not p['label']:
      p.template = site_config['path'] + 'templates/admin/rights.error.tpl'
    else:
      if 'confirm' in p.form:
        if p.form['confirm'] == 'yes':
          #p.db.query_com('DELETE FROM rel_rights WHERE rid=%d' % (p['rid']))
          #p.db.query_com('DELETE FROM rights WHERE rid=%d' % (p['rid']))
          p.template = site_config['path'] + 'templates/admin/rights.delete_yes.tpl'
        else:
          p.template = site_config['path'] + 'templates/admin/rights.delete_no.tpl'
      else:
        p.template = site_config['path'] + 'templates/admin/rights.delete_confirm.tpl'

def insert():
  if not len(p.form['r_category']):
    p['errors']['r_category'] = 'Kategori boş bırakılamaz.'
    
  if not len(p.form['r_keyword']):
    p['errors']['r_keyword'] = 'Kategori boş bırakılamaz.'
  elif p.db.scalar_query('SELECT Count(*) FROM rights WHERE keyword="%s"' % (p.db.escape(p.form['r_keyword'] ) )) > 0:
    p['errors']['r_keyword'] = 'Bu isimde bir kod zaten var.'
    
  if not len(p.form['r_label']):
    p['errors']['r_label'] = 'Etiket boş bırakılamaz.'
      
  if not len(p['errors']):
    p['label'] = p.form['r_label']
    p['rid'] = p.db.insert('rights', {'category': p.form['r_category'], 'keyword': p.form['r_keyword'], 'label': p.form['r_label']})
    p.template = site_config['path'] + 'templates/admin/rights.insert.tpl'
  else:
    p.template = site_config['path'] + 'templates/admin/rights.tpl'
    index()


p.actions = {'default': index,
             'delete': delete,
             'insert': insert}

p.build()
