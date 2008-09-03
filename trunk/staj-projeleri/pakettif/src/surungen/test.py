from kertenkele import *
import time

def selectTest():
    yumurta = Kertenkele('test')
    result = yumurta.dbi.get_packages_of('usr')
    for row in result:
        print row
        time.sleep(1)

def crawlTest():
    yumurta = Kertenkele('test')
    yumurta.dbi.create_table()
    yumurta.insert_all_installed_packages()
    yumurta.dbi.create_index()