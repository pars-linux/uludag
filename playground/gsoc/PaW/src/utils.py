import subprocess

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
        template_contents = template_contents.replace('{%s}' % key, str(value))

    return template_contents


def run_shell_cmd(cmdargs, shell = False, stdout = subprocess.PIPE,
    stderr = subprocess.PIPE):
    '''
    This is a blocking method and may take a long time to complete.
    Use this with a threading instance or twisted library.
    '''
    print ' '.join(cmdargs)

    sp = subprocess.Popen(
        args = cmdargs,
        stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
        shell = shell
    )

    retcode = sp.wait() # wait until process returns
    # TODO: all those can be replaced with subprocess.call(cmdargs) or check_call

    if retcode == 0:
        if sp.stdout:
            return sp.stdout.read()
    else:
        log.exception("Error code returned from shell executable:[%s]||return code: %d||stderr=%s||stdout=%s||"
            % (' '.join(cmdargs), retcode, sp.stderr.read(), sp.stdout.read()))

# Simple Levenshtein Distance snippet.
# Author: Magnus Lie Hetland <magnus at hetland.org>
# Source: http://hetland.org/coding/
# License: LICENSE PENDING
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n

    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]
