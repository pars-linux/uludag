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

    def installationRegistry(self):
        # TODO: InstallLocation, DisplayIcon, Comments
        uninstallString = 'defrag.exe'

        self.reg.CreateKey(
          hDefKey=_winreg.HKEY_LOCAL_MACHINE,
          sSubKeyName=self.hlmPath)

        log.debug(self.hlmPath + ' registry key created.')

        self.reg.SetStringValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE,sSubKeyName = self.hlmPath,
          sValueName = 'DisplayName', sValue = self.mainEngine.application)

        self.reg.SetStringValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE,sSubKeyName = self.hlmPath,
          sValueName = 'DisplayVersion', sValue = self.mainEngine.version)

        self.reg.SetStringValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE, sSubKeyName = self.hlmPath,
          sValueName = 'UninstallString', sValue = uninstallString)

        self.reg.SetStringValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE, sSubKeyName = self.hlmPath,
          sValueName = 'HelpLink', sValue = self.mainEngine.home)

        self.reg.SetStringValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE, sSubKeyName = self.hlmPath,
          sValueName = 'URLInfoAbout', sValue = self.mainEngine.home)

        self.reg.SetStringValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE, sSubKeyName = self.hlmPath,
          sValueName = 'Publisher', sValue = self.mainEngine.home)

        self.reg.SetDWORDValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE, sSubKeyName = self.hlmPath,
          sValueName = 'NoModify', uValue = 1)

        self.reg.SetDWORDValue(
          hDefKey = _winreg.HKEY_LOCAL_MACHINE, sSubKeyName = self.hlmPath,
          sValueName = 'NoRepair', uValue = 1)

        log.debug('Registry subkeys have been created.')

    def uninstallationRegistry(self):
        self.reg.DeleteKey(hDefKey=_winreg.HKEY_LOCAL_MACHINE, sSubKeyName=self.hlmPath)
        log.debug('Registry subkey has been removed successfully.')

    def ejectCD(self):
        # If CD/DVD is used, eject it after installation.
        pass

    def reboot(self):
        self.wmi.Win32_OperatingSystem(Primary = 1)[0].Reboot()

    def getTempFolder(self):
        pass

    def getInstallationPath(self):
        pass
