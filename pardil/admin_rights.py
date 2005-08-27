#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config
import re

p = pardil_page()

p.name = 'pardil_admin_rights'
p.title = site_config['title']

# OLMAZSA OLMAZ!
if 'sid' not in p['session']:
  p.http.redirect('error.py?tag=login_required')
if not p.access('administrate'):
  p.http.redirect('error.py?tag=not_in_authorized_group')
# OLMAZSA OLMAZ!

def index():
  p['rights'] = []
  q = """SELECT
           rid, category, keyword, label
         FROM rights
         ORDER BY rid ASC
      """
  list = p.db.query(q)
  for i in list:
    l = {
         'rid': i[0],
         'category': i[1],
         'keyword': i[2],
         'label': i[3]
         }
    p['rights'].append(l)

  p.template = 'admin/rights.tpl'

def delete():
  if 'rid' in p.form and re.match('^[0-9]+$', p.form['rid']):
    p['rid'] = int(p.form['rid'])
  else:
    p.template = 'admin/rights.error.tpl'
    return
    
  q = """SELECT
           label
         FROM rights
         WHERE rid=%d
      """ % (p['rid'])
  p['label'] = p.db.scalar_query(q)

  if not p['label']:
    p.template = 'admin/rights.error.tpl'
  else:
    if 'confirm' in p.form:
      if p.form['confirm'] == 'yes':
        #p.db.query_com('DELETE FROM rel_rights WHERE rid=%d' % (p['rid']))
        #p.db.query_com('DELETE FROM rights WHERE rid=%d' % (p['rid']))
        p.template = 'admin/rights.delete_yes.tpl'
      else:
        p.template = 'admin/rights.delete_no.tpl'
    else:
      p.template = 'admin/rights.delete_confirm.tpl'

def insert():
  if 'r_category' not in p.form or not len(p.form['r_category']):
    p['errors']['r_category'] = 'Kategori boş bırakılamaz.'
    
  if 'r_keyword' not in p.form or not len(p.form['r_keyword']):
    p['errors']['r_keyword'] = 'Erişim kodu boş bırakılamaz.'
  else:
    q = """SELECT Count(*)
           FROM rights
           WHERE keyword="%s"
        """ % (p.db.escape(p.form['r_keyword']))
    if p.db.scalar_query(q) > 0:
      p['errors']['r_keyword'] = 'Bu isimde bir kod zaten var.'
    
  if 'r_label' not in p.form or not len(p.form['r_label']):
    p['errors']['r_label'] = 'Etiket boş bırakılamaz.'
      
  if not len(p['errors']):
    p['label'] = p.form['r_label']
    
    list = {
            'category': p.form['r_category'],
            'keyword': p.form['r_keyword'],
            'label': p.form['r_label']
            }
    p['rid'] = p.db.insert('rights', list)

    p.template = 'admin/rights.insert.tpl'
  else:
    p.template = 'admin/rights.tpl'
    index()


p.actions = {
             'default': index,
             'delete': delete,
             'insert': insert
             }

p.build()
