import os.path
import subprocess
import os

from logger import getLogger
log = getLogger('Utils')

sizeUnits = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
timeUnitsSingle = ['second', 'minute', 'hour', 'day']
timeUnitsPlural = ['seconds', 'minutes', 'hours', 'days']

def humanReadableSize(bytes):
    global sizeUnits

    bytes = long(bytes)
    x = 0
    part = 0
    while bytes/1024>0:
	x += 1
	part = int((bytes % 1024)/1024.0*100)
	bytes >>= 10
    return '%d.%d %s' % (bytes, part, sizeUnits[x])

def humanReadableTime(seconds):
    global timeUnitsSingle
    global timeUnitsPlural

    if seconds>=24*60*60:
	v1=seconds/(24*60*60)
	v2=(seconds%(24*60*60))/(60*60)
	u1=3
	u2=2
    elif seconds>=60*60:
	v1=seconds/(60*60)
	v2=(seconds%(60*60))/(60)
	u1=2
	u2=1
    elif seconds>=60:
	v1=seconds/(60)
	v2=(seconds%(60))
	u1=1
	u2=0
    else:
	v1=0
	v2=seconds%(60)
	u1=1
	u2=0

    if(v1==1): u1 = timeUnitsSingle[u1]
    else: u1 = timeUnitsPlural[u1]
    if(v2==1): u2 = timeUnitsSingle[u2]
    else: u2 = timeUnitsPlural[u2]


    return '%d %s %d %s' % (v1,u1,v2,u2)


def populate_template_file(path, values):
    try:
        ifstream = open(path, 'r')
        template_contents = ifstream.read()
        ifstream.close()
    except:
        return False

    return populate_template(template_contents, values)

def populate_template(template_contents, values):
    for key,value in values.iteritems():
        template_contents = template_contents.replace('{%s}' % key, value)

    return template_contents


def run_shell_cmd(cmdargs, shell = False):
    '''
    This is a blocking method and may take a long time to complete.
    Use this with a threading instance or twisted library.
    '''

    if isinstance(cmdargs, list):
        cmdargs[0] = os.path.normpath(os.path.abspath(cmdargs[0]))

    sp = subprocess.Popen(
        args = cmdargs,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell = shell
    )

    retcode = sp.wait() # wait until process returns
    # TODO: all those can be replaced with subprocess.call(cmdargs) or check_call

    if retcode == 0:
        return sp.stdout.read()
    else:
        log.exception("Error code returned from shell executable:[%s]||return code: %d||stderr=%s||stdout=%s||"
            % (' '.join(cmdargs), retcode, sp.stderr.read(), sp.stdout.read()))
