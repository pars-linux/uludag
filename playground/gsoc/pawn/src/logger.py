import logging

def getLogger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    log.addHandler(ch)
    return log
