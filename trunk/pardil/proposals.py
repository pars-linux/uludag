#!/usr/bin/python
# -*- coding: utf-8 -*-

from pardilskel import pardil_page
from cfg_main import site_config

p = pardil_page()

p.name = 'pardil_proposals'
p.title = site_config['title']

def index():
  versions = []
  q = """SELECT max(vid)
         FROM proposals_versions
         GROUP BY pid
      """
  for row in p.db.query(q):
    versions.append(str(row[0]))

  p['proposals'] = []
  if len(versions):
    q = """SELECT
             proposals.pid AS _pid,
             proposals_versions.version,
             proposals_versions.title
           FROM proposals
             INNER JOIN proposals_versions
               ON proposals.pid=proposals_versions.pid
           WHERE
             proposals_versions.vid IN (%s)
           ORDER BY proposals.pid ASC
        """ % (','.join(versions))
    list = p.db.query(q)
    for i in list:
      l = {
           'pid': i[0],
           'version': i[1],
           'title': i[2]
           }
      p['proposals'].append(l)

  p.template = 'proposals.tpl'

p.actions = {'default': index}
p.build()
