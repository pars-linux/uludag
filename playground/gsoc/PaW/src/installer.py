import tempfile
import os
from utils import *

from logger import getLogger
log = getLogger('Installer Backend')

try:
    from wmi import wmi
    import _winreg
except ImportError, NameError:
    log.debug('Could not import _winreg. Missing module.')

class Installer():
    grub_loader_file = 'parldr'

    def __init__(self, mainEngine):
        self.mainEngine = mainEngine

        try:
            self.wmi = wmi.WMI(privileges=["Shutdown"])
            self.reg = wmi.WMI(namespace="DEFAULT").StdRegProv
        except:
            log.warning("Could not use WMI. Most probably on Linux.")

        try:
            self.hlmPath = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\" + self.mainEngine.appid
        except AttributeError:
            pass # supress

        self.setTempFolder()
        self.setTempFile()

    def _setRegistryKey(self, hlmPath, keyName, keyValue, isDWORD = False):
        try:
            if isDWORD:
                self.reg.SetDWORDValue(hDefKey = _winreg.HKEY_LOCAL_MACHINE,
                  sSubKeyName = hlmPath, sValueName = keyName, uValue = keyValue)
            else:
                self.reg.SetStringValue(hDefKey = _winreg.HKEY_LOCAL_MACHINE,
                  sSubKeyName = hlmPath, sValueName = keyName, sValue = keyValue)
        except:
            log.exception('Could not set registry key %s.' % keyName)


    def installationRegistry(self):
        # TODO: InstallLocation, DisplayIcon, Comments
        uninstallString = 'defrag.exe'

        try:
            self.reg.CreateKey(hDefKey=_winreg.HKEY_LOCAL_MACHINE,
              sSubKeyName=self.hlmPath)
            log.debug(self.hlmPath + ' registry key is created.')
        except:
            log.exception(self.hlmPath + ' registry key could not be created.')

        self._setRegistryKey(self.hlmPath, 'DisplayName', self.mainEngine.application)
        self._setRegistryKey(self.hlmPath, 'DisplayVersion', self.mainEngine.version)
        self._setRegistryKey(self.hlmPath, 'UninstallString', uninstallString)
        self._setRegistryKey(self.hlmPath, 'HelpLink', self.mainEngine.home)
        self._setRegistryKey(self.hlmPath, 'URLInfoAbout', self.mainEngine.home)
        self._setRegistryKey(self.hlmPath, 'Publisher', self.mainEngine.home)
        self._setRegistryKey(self.hlmPath, 'NoModify', 1, True)
        self._setRegistryKey(self.hlmPath, 'NoRepair', 1, True)

    def uninstallationRegistry(self):
        try:
            self.reg.DeleteKey(hDefKey=_winreg.HKEY_LOCAL_MACHINE, sSubKeyName=self.hlmPath)
            log.debug('Registry subkey has been removed successfully.')
        except:
            log.exception('Could not remove registry keys upon uninstallation.')

    def ejectCD(self):
        # If CD/DVD is used, eject it after installation.
        pass

    def reboot(self):
        self.wmi.Win32_OperatingSystem(Primary = 1)[0].Reboot()

    def setTempFolder(self):
        self.mainEngine.config.tmpDir = tempfile.mkdtemp()

    def setTempFile(self):
        self.mainEngine.config.isoFile = \
            os.path.join(self.mainEngine.config.tmpDir, 'downloaded.iso')

    def getInstallationRoot(self):
        return os.path.join(self.mainEngine.config.drive, self.mainEngine.appid)

    def getGrubLoaderDestination(self):
        system_drive_root = '%s\\'% self.mainEngine.compatibility.OS.SystemDrive
        return os.path.join(system_drive_root, self.grub_loader_file)

    def modify_boot_ini(self):
        # read boot.ini
        fstream = None
        system_drive_root = '%s\\'% self.mainEngine.compatibility.OS.SystemDrive
        boot_ini_path = os.path.join(system_drive_root,'boot.ini')
        # TODO: Fail-safe and better path join.

        if not os.path.isfile(boot_ini_path):
            log.exception('Could not locate boot.ini')
            return

        # make boot.ini editable.
        attrib_path = os.path.join(os.getenv('WINDIR'), 'System32', 'attrib.exe')
        run_shell_cmd([attrib_path, '-S', '-H', '-R', boot_ini_path])

        try:
            fstream = open(boot_ini_path, 'r') #reading stream
            contents = fstream.read()
            fstream.close()
        except:
            log.exception('Could not open boot.ini file for reading and writing.')
            return

        config = {
            'OLD_CONTENTS' : contents,
            'GRUB_LOADER_PATH' : self.getGrubLoaderDestination(),
            'OPTION_NAME' : self.mainEngine.application
        }
        
        new_contents = populate_template_file('files/boot.ini.tpl', config)

        if fstream:
            try:
                fstream = open(boot_ini_path, 'w') # writing stream
                fstream.write(new_contents)
                log.debug('New boot.ini contents are written.')
            except IOError, err:
                log.exception('IOError on updating: %s' % str(err))
            finally:
                fstream.close()
        else:
            log.exception('Could not write boot.ini file.')

        # restore system+readonly+hidden attribs of boot.ini
        run_shell_cmd([attrib_path, '+S', '+H', '+R', boot_ini_path])
