import time

def now():
  return int(time.time())

def sql_date(t):
  return time.strftime('%Y-%m-%d', time.gmtime(t))

def sql_datetime(t):
  return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t))
