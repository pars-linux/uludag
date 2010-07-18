import sys
import logging

destination = 'log.log' # changed by PaW class later.

def getLogger(name):
    """
    Returns a logger with given name. If the executable is not standalone,
    logging output will be streamed to stdout and stderr, if the executable
    is standalone (has no 'python' occurrence in its full path) output will
    be streamed to file determined dynamically by __main__ file and can be
    reached via PaW.logfile (appeared as self.mainEngine.logfile in most cases.)
    """
    global destination

    try:
        if sys.executable.lower().index('python') > -1:
            logfile = None
    except:
        logfile = destination

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=logfile,
                    filemode='w')
                    
    log = logging.getLogger(name)
    
    return log