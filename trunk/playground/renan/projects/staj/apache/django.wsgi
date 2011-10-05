import os
import sys

path = '/home/pars/workspace'
path2 = '/home/pars/workspace/staj'
path3 = '/home/pars/workspace/staj/form'
if path not in sys.path:
    sys.path.append(path)

if path2 not in sys.path:
    sys.path.append(path2)

if path3 not in sys.path:
    sys.path.append(path3)

os.environ['DJANGO_SETTINGS_MODULE'] = 'staj.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
