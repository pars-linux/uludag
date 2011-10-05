import datetime
from django.shortcuts import render_to_response
import MySQLdb

def test(request):
    db = MySQLdb.connect(user='root', db='root', passwd='12345', host='localhost')
    cursor = db.cursor()
    cursor.execute('select * from mytable')
    names = [row[0] for row in cursor.fetchall()]
    db.close()
    return render_to_response('form.html', {'names': names})


def tmplt(request):
    name = 'pardus'
    surname = 'pardus'
    return render_to_response('form.html', locals())
