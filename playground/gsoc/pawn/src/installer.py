from wmi import wmi

from logger import getLogger
log = getLogger('Installer Backend')

try:
    import _winreg
except ImportError:
    log.debug('Could not import _winreg. Missing module.')

class Installer():
    def __init__(self, mainEngine):
        self.mainEngine = mainEngine
        self.wmi = wmi.WMI(privileges=["Shutdown"])
        self.reg = wmi.WMI(namespace="DEFAULT").StdRegProv
        self.hlmPath = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\" + self.mainEngine.appid


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

    def getTempFolder(self):
        pass

    def getInstallationPath(self):
        pass
