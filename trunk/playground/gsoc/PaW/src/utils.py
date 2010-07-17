import subprocess
import os
import ConfigParser

from logger import getLogger
log = getLogger('Utils')

sizeUnits = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
timeUnitsSingle = ['second', 'minute', 'hour', 'day']
timeUnitsPlural = ['seconds', 'minutes', 'hours', 'days']

def humanReadableSize(bytes):
    """
    Converts bytes to human readable size units.
    """
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
    """
    Converts seconds to human readable time scale. Upper unit is days.
    """
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
    """
    Populates the given template file with the values and return new contents.
    """
    try:
        ifstream = open(path, 'r')
        template_contents = ifstream.read()
        ifstream.close()
    except:
        return False

    return populate_template(template_contents, values)

def populate_template(template_contents, values):
    """
    Populates the given template contents as string and returns back the
    new contents.
    """

    for key,value in values.iteritems():
        template_contents = template_contents.replace('{%s}' % key, str(value))

    return template_contents


def run_shell_cmd(cmdargs, shell = False, stdout = subprocess.PIPE,
    stderr = subprocess.PIPE):
    '''
    This is a blocking method and may take a long time to complete.
    Use this with a threading instance or twisted library.
    '''

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
# License: Author has permitted of usage upon private request.
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b. Case-sensitive."
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


def locate_file_in_path(path, filename):
    """
    Locates first occurrence of given file with 'filename' parameter
    by searching recursively in given path (this can be a CD-DVD or USB
    drive root. First, root is scanned then subfolders are scanned according
    to their names in ascending order. This is a depth-first search.
    """
    try:
        contents = os.listdir(path)
    except:
        return None # device may not be ready or unexisting path.

    try: index = contents.index(filename)
    except ValueError: index = -1 # indicates does not exist here.

    if not index == -1 and os.path.isfile(os.path.join(path,filename)):
        return os.path.join(path, filename)
    else:
        for item in contents:
            if os.path.isdir(os.path.join(path, item)): # nested dirs
                result = locate_file_in_path(os.path.join(path,item), filename)
                if result: return result
    return None

def version_name_from_gfxboot(gfxboot_cfg_path):
    """
    Returns distro name by parsing given gfxboot.cfg file at absolute path of
    gfxboot_cfg_path. This file is most probably in the installation CD.
    """
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(gfxboot_cfg_path)
    distro_name = config_parser.get('base','distro')
    return distro_name

def boot_ini_cleaner(boot_ini_path, grldr_name):
    """
    Cleans line including grldr_name from given boot.ini file and writes
    back the rest of the original file. Returns False if any errors occur on
    reading/writing, True if writeback is done successfully.
    """
    try:
        f = open(boot_ini_path, 'r')
        log.error('Could not read %s file for cleanup: %s' % (boot_ini_path, e))
    except IOError as e:
        return False

    new_boot_ini = ''
    for line in f:
        try:
            if line.index(grldr_name) > -1:
                pass
        except ValueError:
            new_boot_ini += line
    
    if f and not f.closed:
        f.close()

    try:
        f = open(boot_ini_path, 'w')
        f.write(new_boot_ini)
        f.close()
        return True
    except IOError as e:
        log.error('Could not write to %s file for cleanup: %s' % (boot_ini_path, e))
        return False