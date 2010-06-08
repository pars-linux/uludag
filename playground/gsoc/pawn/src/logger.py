import logging

def getLogger(name):
    log = logging.getLogger(name)
    ch = logging.StreamHandler()
    log.addHandler(ch)
    return log
