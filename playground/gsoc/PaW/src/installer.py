import os
import shutil
import ctypes
import tempfile
from taskrunner import Task
from taskrunner import TaskList

from utils import populate_template_file
from utils import run_shell_cmd

from logger import getLogger
log = getLogger('Installer Backend')

try:
    from tools.wmi import wmi
    import _winreg
except ImportError, NameError:
    log.debug('Could not import _winreg or wmi. Missing module.')

class Installer():
    gui = None
    iso_extractor = "c:\\Progra~1\\Utils\\7-Zip\\7z.exe" # TODO: test purposes.
    
    grub_default_timeout = 0
    grub_loader_file = 'grldr'
    grub_loader_path = '/grldr'
    grub_mbr_file = 'grldr.mbr'
    grub_mbr_path = '/grldr.mbr'
    grub_identifier_file = 'pardus.tag'
    grub_identifier_path = '/pardus.tag'

    default_kernel_path = 'boot/kernel'
    default_kernel_params = ''
    default_initrd_path = 'boot/initrd'
    default_img_path = 'pardus.img'

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

    def _setRegistryKey(self, hlmPath, keyName, keyValue, isDWORD=False):
        try:
            if isDWORD:
                self.reg.SetDWORDValue(hDefKey=_winreg.HKEY_LOCAL_MACHINE,
                                       sSubKeyName=hlmPath, sValueName=keyName, uValue=keyValue)
            else:
                self.reg.SetStringValue(hDefKey=_winreg.HKEY_LOCAL_MACHINE,
                                        sSubKeyName=hlmPath, sValueName=keyName, sValue=keyValue)
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
        "If CD/DVD is used, eject CD/DVD-ROM tray after installation."
        # TODO: Known bug, only ejects first CD-ROM drive tray.
        try:
            return bool(ctypes.windll.WINMM.mciSendStringW(u"set cdaudio door open", None, 0, None))
        except:
            return False

    def reboot(self):
        self.wmi.Win32_OperatingSystem(Primary=1)[0].Reboot()

    def setTempFolder(self):
        self.mainEngine.config.tmpDir = tempfile.mkdtemp()

    def setTempFile(self):
        self.mainEngine.config.isoFile = \
            os.path.join(self.mainEngine.config.tmpDir, 'downloaded.iso')

    def getInstallationRoot(self):
        return os.path.join(self.mainEngine.config.drive.DeviceID + '\\', self.mainEngine.appid)

    def getGrubLoaderDestination(self):
        system_drive_root = '%s\\' % self.mainEngine.compatibility.OS.SystemDrive
        return os.path.join(system_drive_root, self.grub_loader_file)

    def modify_boot_ini(self):
        """
        Windows 2000, Windows XP, Windows 2003 Server has boot.ini under primary
        partition. We simply append c:\grldr="Pardus" to launch grub4dos from
        ntldr (Windows NT Loader).
        """
        # read boot.ini
        fstream = None
        system_drive_root = '%s\\' % os.getenv('SystemDrive')
        # alternative is self.mainEngine.compatibility.OS.SystemDrive
        boot_ini_path = os.path.join(system_drive_root, 'boot.ini')
        # TODO: Fail-safe and better path join.

        if not os.path.isfile(boot_ini_path):
            log.exception('Could not locate boot.ini')
            return False

        # make boot.ini editable.
        attrib_path = os.path.join(os.getenv('WINDIR'), 'System32', 'attrib.exe')
        run_shell_cmd([attrib_path, '-S', '-H', '-R', boot_ini_path])

        try:
            fstream = open(boot_ini_path, 'r') #reading stream
            contents = fstream.read()
            fstream.close()
        except:
            log.exception('Could not open boot.ini file for reading and writing.')
            return False

        config = {
            'OLD_CONTENTS': contents,
            'GRUB_LOADER_PATH': self.getGrubLoaderDestination(),
            'OPTION_NAME': self.mainEngine.application
        }

        new_contents = populate_template_file('files/boot.ini.tpl', config)

        if fstream:
            try:
                fstream = open(boot_ini_path, 'w') # writing stream
                fstream.write(new_contents)
                log.debug('New boot.ini contents are written.')
            except IOError, err:
                log.exception('IOError on updating: %s' % str(err))
                return False
            finally:
                fstream.close()

        # restore system+readonly+hidden attribs of boot.ini
        run_shell_cmd([attrib_path, '+S', '+H', '+R', boot_ini_path])
        return True

    def modify_bcd(self):
        """
        For Windows Vista and Windows 7, we use bcdedit command to launch
        grub4dos from boot sector. bcdedit.exe is under System32 folder.
        For more, see http://grub4dos.sourceforge.net/wiki/index.php/Grub4dos_tutorial#Booting_GRUB_for_DOS_via_the_Windows_Vista_boot_manager

        bcdedit /create /d "Start GRUB4DOS" /application bootsector
        bcdedit /set {id} device boot
        bcdedit /set {id} path \grldr.mbr
        bcdedit /displayorder {id} /addlast
        """

        bcdedit_paths = [# possible paths for bcdedit.
            os.path.join(os.getenv('SystemDrive') + '\\', 'Windows', 'System32', 'bcdedit.exe'),
            os.path.join(os.getenv('windir'), 'System32', 'bcdedit.exe'),
            os.path.join(os.getenv('systemroot'), 'System32', 'bcdedit.exe'),
            os.path.join(os.getenv('windir'), 'sysnative', 'bcdedit.exe'),
            os.path.join(os.getenv('systemroot'), 'sysnative', 'bcdedit.exe')
            ]

        for path in bcdedit_paths:
            if os.path.isfile(path):
                bcdedit_path = path
                break
            else:
                bcdedit_path = None

        if not bcdedit_path:
            log.exception('Could not locate bcdedit.exe')
            return

        guid = run_shell_cmd([bcdedit_path, '/create', '/d', self.mainEngine.application, '/application', 'bootsector'])
        # TODO: replace app name
        guid = guid[guid.index('{'): guid.index('}') + 1] # fetch {...} guid from message string

        config_commands = [
            [bcdedit_path, '/set', guid, 'device', 'boot'],
            [bcdedit_path, '/set', guid, 'path', '\\grldr.mbr'],
            [bcdedit_path, '/displayorder', guid, '/addlast']
        ]

        for cmd in config_commands:
            run_shell_cmd(cmd)

        self.mainEngine.config.bcd_guid = guid
        # TODO: save bcd_guid to the REGISTRY
        log.debug('bcdedit record created successfully.')
        return True

    def extract_from_iso(self, source, destination, file_paths):
        """
        For 7z, file paths should be specified as a/b/c
        Instead of file path 'list', single file path entry is also OK.
        """
        if not isinstance(file_paths, list): file_paths = [file_paths]

        executable = self.iso_extractor
        destination = os.path.abspath(destination)
        source = os.path.abspath(source)

        if not os.path.isfile(executable):
            log.error('Could not file ISO extractor executable.')
            return False

        if not os.path.isfile(source):
            log.error('Could not find ISO file.')
            return False

        if not os.path.isdir(destination):
            log.error('Could not find destination folder.')
            return False

        # TODO: CRITICAL-TBD
        # ' '.join(file_path) in command list doesn't work with subprocess according
        # to stdout output. However ' '.join-ing shell commands and obtaining a
        # string and running it on shell works perfectly. However, when file_paths
        # has only 1 item, it works. so for now, we switch to foreach statement.
        # This is not good for performance, as expected.
        for file_path in file_paths:
            run_shell_cmd([executable, 'e', '-o' + destination, '-y', source, file_path])
            log.debug('Extracted: %s' % file_path)

        return True

    def createDirStructure(self):
        "Creates directory structure on installation drive."
        base = self.getInstallationRoot()

        self.mainEngine.config.installationRoot = base

        dirs = [
            '.',
            'boot',
            'help',
            'log']

        for dir in dirs:
            path = os.path.join(base, dir)
            try:
                os.mkdir(path)
                log.debug('%s created.' % path)
            except OSError:
                log.debug('%s already exists.' % path)

        return True

    def copy_cd_files(self):
        cd_root = self.mainEngine.config.cdDrive.DeviceID + '\\'
        destination = os.path.abspath(os.path.join(self.getInstallationRoot(), 'boot'))

        if self.mainEngine.version:
            files = [
                self.mainEngine.version.kernel, self.mainEngine.version.initrd,
                self.mainEngine.version.img]
        else:
            log.warning('Could not recognize version. Using default CD paths.')
            files = [self.default_kernel_path, self.default_initrd_path,
                self.default_img_path]

        for file_path in files:
            path = os.path.abspath(os.path.join(cd_root, file_path))
            if not os.path.isfile(path):
                log.error('Could not locate %s' % path)
                return False

            try:
                shutil.copy(path, destination)
                log.debug('%s copied to %s' % (path, destination))
            except IOError as e:
                log.error('Could not copy: %s' % e); return False
        return True

    def modify_boot_sequence(self):
        winMajorVersion = self.mainEngine.compatibility.winMajorVersion()

        if winMajorVersion < 6:
            # Windows 2000, XP, Server 2003. <5 already prevented to install.
            log.debug('Detected Windows 2000, XP or Server 2003.')
            return self.modify_boot_ini()
        else:
            # Windows Vista, Windows 7 or newer.
            log.debug('Detected Windows Vista, Windows 7 or newer.')
            return self.modify_bcd()

    def copy_grub4dos_files(self):
        os_drive = self.mainEngine.compatibility.OS.SystemDrive
        destination = os.path.abspath(os_drive + '\\')
        source = os.path.abspath(os.path.join('files', 'grub4dos'))

        # prepare menu.lst template
        if self.mainEngine.version:
            log.info('Preparing menu.lst for %s' % self.mainEngine.version.name)
            values = {
                'TIMEOUT': self.grub_default_timeout,
                'DISTRO': self.mainEngine.version.name,
                'IDENTIFIER_PATH': self.grub_identifier_path,
                'PATH_KERNEL': '/'.join(['', self.mainEngine.appid, 'boot',
                                        os.path.basename(self.mainEngine.version.kernel)]),
                'KERNEL_PARAMS': self.mainEngine.version.kernelparams,
                'PATH_INITRD': '/'.join(['', self.mainEngine.appid, 'boot',
                                        os.path.basename(self.mainEngine.version.initrd)])
            }
        else:
            log.info('Preparing menu.lst using hardcoded default values')
            values = {
                'TIMEOUT': self.grub_default_timeout,
                'DISTRO': self.mainEngine.appid,
                'IDENTIFIER_PATH': self.grub_identifier_path,
                'PATH_KERNEL': '/'.join(['', self.mainEngine.appid, 'boot',
                                        os.path.basename(self.default_kernel_path)]),
                'KERNEL_PARAMS': self.default_kernel_params,
                'PATH_INITRD': '/'.join(['', self.mainEngine.appid, 'boot',
                                        os.path.basename(self.default_initrd_path)])
            }

        # save menu.lst under OS drive root.
        menu_lst_dest = os.path.join(destination, 'menu.lst')
        menu_lst = populate_template_file(os.path.join(source, 'menu.lst.tpl'), values)
        try:
            menu_lst_stream = open(menu_lst_dest, 'w')
            menu_lst_stream.write(menu_lst)
            menu_lst_stream.close
            log.debug('%s created successfully.' % menu_lst_dest)
        except IOError as e:
            log.error('Could not write %s. %s' % (menu_lst_dest, e)); return False

        # copy rest of grub4dos files
        files = [self.grub_loader_file, self.grub_mbr_file, self.grub_identifier_file]
        for file_name in files:
            path = os.path.abspath(os.path.join(source, file_name))
            if not os.path.isfile(path):
                log.error('Could not locate %s' % path); return False
            try:
                shutil.copy(path, destination)
                log.debug('%s copied to %s' % (os.path.basename(path), destination))
            except IOError as e:
                log.error('Could not copy grub4dos file %s: %s' % (path,e)); return False
        return True

    def start(self):
        "Starts installation process specific for ISOs and CD/DVDs."
        self.tasklist = TaskList(callback=self.onAdvance)
        
        if hasattr(self.mainEngine.config, 'isoPath'):
            tasks = self.get_iso_installation_tasks(self.tasklist)
        else:
            tasks = self.get_cd_installation_tasks(self.tasklist)

        self.tasklist.setTasks(tasks)
        self.tasklist.start()

    def onAdvance(self):
        percentage = self.tasklist.getPercentage()
        if self.gui: self.gui.onAdvance(percentage)

    def connectGui(self, gui):
        self.gui = gui

    def get_cd_installation_tasks(self, associated_tasklist):
        cb = associated_tasklist.startNext # callback

        def foo():pass

        return [
            Task(self.createDirStructure, 'Creating directory structure', cb),
            Task(self.copy_cd_files, 'Copying files from CD', cb),
            Task(self.copy_grub4dos_files, 'Copying and preparing GRUB files', cb),
            Task(foo, 'Copying uninstallation files', cb),
            Task(foo, 'Creating Registry keys', cb),
            Task(self.modify_boot_sequence, 'Modifying Windows boot configuration', cb),
            Task(foo, 'Cleanup after installation', cb),
            Task(foo, 'Ejecting CD tray', cb),
        ]

    def get_iso_installation_tasks(self, associated_tasklist):
        return []
