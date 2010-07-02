import logging

def getLogger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    log.addHandler(ch)
    return log
