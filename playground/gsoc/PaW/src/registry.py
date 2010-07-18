from _winreg import *

import logger
log = logger.getLogger('Registry Handler')

try:
    import _winreg
except ImportError, NameError:
    log.debug('Could not import _winreg or wmi. Missing module.')

def hCreateKey(hlmPath):
    "Naive function to create a key under HKLM."
    return CreateKey(HKEY_LOCAL_MACHINE, hlmPath)

def hDeleteKey(hlmPath):
    "Naive function to delete a key from HKLM."
    DeleteKey(HKEY_LOCAL_MACHINE, hlmPath)

def hGetKey(hlmPath):
    return OpenKey(HKEY_LOCAL_MACHINE, hlmPath, 0, KEY_ALL_ACCESS)

def hSetValue(key, keyName, keyValue, isDWORD = False):
    """Creates a value under specified 'hlmPath' key. If isDWORD is true then
    value is REG_DWORD, otherwise REG_SZ."""

    if isinstance(key, str):
        key = hGetKey(key)

    if isDWORD:
        valtype = REG_DWORD
        keyValue = int(keyValue)
    else:
        valtype = REG_SZ
        keyValue = str(keyValue)
    
    SetValueEx(key, keyName, 0, valtype, keyValue)
    key = None