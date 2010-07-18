import os
import sys
import shutil
import ctypes
import registry
import time
from ConfigParser import RawConfigParser
from taskrunner import Task
from taskrunner import TaskList
from utils import populate_template_file
from utils import run_shell_cmd
from utils import backup_bcdedit
from utils import copy_folder

import logger
log = logger.getLogger('Installer Backend')

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
    menu_lst_template_file = 'menu.lst.tpl'
    menu_lst_file = 'menu.lst'
    boot_ini_template_file = 'boot.ini.tpl'

    default_kernel_path = 'boot/kernel'
    default_kernel_params = ''
    default_initrd_path = 'boot/initrd'
    default_img_path = 'pardus.img'

    cfg_file = "pardus.ini"
    boot_ini_backup_file = "boot.ini.bak"
    bcdedit_backup_file = "bcdedit.bak"

    def __init__(self, mainEngine):
        "Initialize installer instance."
        self.mainEngine = mainEngine

        try:
            self.hlmPath = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\" + self.mainEngine.appid
        except AttributeError as e:
            log.error('Error initializing HLM Path: %s' % e)
            pass # supress


    def hasRegistryKey(self):
        """
        Returns True if there already exist a registry key which should be
        created by installationRegistry() method. Indicates there has been a
        previous attempt to install PaW, or it is already installed.
        Handles WindowsError exception which is thrown upon the request of
        unexisting registry path. Returns False, in this case.
        """
        try:
            key = registry.hGeztKey(self.hlmPath)
            if key: return True
            else: return False
        except: return False


    def installationRegistry(self):
        """
        Creates installation registry keys and values on Windows registry.
        """
        try:
            key = registry.hCreateKey(self.hlmPath)
        except Exception as e:
            log.exception(self.hlmPath + ' registry key could not be created: %s' % e)
            return False

        registry.hSetValue(key, 'DisplayName', self.mainEngine.application)
        registry.hSetValue(key, 'DisplayVersion', self.mainEngine.appversion)
        registry.hSetValue(key, 'UninstallString', self.getUninstallationString())
        registry.hSetValue(key, 'DisplayIcon', self.getDisplayIconPath())
        registry.hSetValue(key, 'HelpLink', self.mainEngine.home)
        registry.hSetValue(key, 'URLInfoAbout', self.mainEngine.home)
        registry.hSetValue(key, 'Publisher', self.mainEngine.publisher)
        registry.hSetValue(key, 'NoModify', 1, True)
        registry.hSetValue(key, 'NoRepair', 1, True)

        log.debug('Finished creating installation registry keys.')
        return True

    def uninstallationRegistry(self):
        "Removes registry key for this program."
        try:
            self.reg.hDeleteKey(self.hlmPath)
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

    def getInstallationRoot(self):
        """
        Returns installation root to copy boot and disk files under it.
        """
        return os.path.join(self.mainEngine.config.drive.DeviceID + '\\', self.mainEngine.appid)


    def getUninstallationString(self):
        """Returns Windows commandline string to uninstall program. Most
        probably will be saved into registry to handle uninstallation."""
        installer_path = os.path.join(self.getInstallationRoot(), 'paw', self.mainEngine.executable)

        uninstall_string = "%s /u" % installer_path
        return uninstall_string

    def getDisplayIconPath(self):
        """
        Returns icon path which is going to be extracted from .exe installer
        file under paw/ folder of installation root."""
        installer_path = os.path.join(self.getInstallationRoot(), 'paw', self.mainEngine.executable)

        return "%s,0" % installer_path

    def getGrubLoaderDestination(self):
        "Returns default grub loader destination, which is in the boot partition."
        system_drive_root = '%s\\' % self.mainEngine.compatibility.OS.SystemDrive
        return os.path.join(system_drive_root, self.grub_loader_file)


    def backup_boot_ini(self, boot_ini_path):
        """
        Backups boot.ini file at given path.
        Precondition: boot_ini_path exists.
        """
        destination = os.path.join(self.getInstallationRoot(), 'backup', boot_ini_backup_file)
        try:
            shutil.copy(boot_ini_path, destination)
        except Exception as e:
            log.error('Could not copy boot.ini: %s' % e)
            return False
        log.debug('Boot.ini backup completed.')
        return True


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

        # Backup bootini file
        self.backup_boot_ini(boot_ini_path)

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

        boot_ini_template_path = \
            os.path.join('files', self.boot_ini_template_file)

        if not os.path.isfile(boot_ini_path):
            #boot.ini may be copied in the same folder with executable
            boot_ini_template_path= os.path.join(self.boot_ini_template_file)

        new_contents = populate_template_file(boot_ini_template_path, config)

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
            return False

        # BACKUP bcdedit boot data configuration to a file before modifying.
        destination_file = os.path.join(self.getInstallationRoot(), 'backup', self.bcdedit_backup_file)
        backup_bcdedit(bcdedit_path, destination_file)

        guid = run_shell_cmd([bcdedit_path, '/create', '/d', self.mainEngine.appid, '/application', 'bootsector'])
        # TODO: replace app name
        guid = guid[guid.index('{'): guid.index('}') + 1] # fetch {...} guid from message string

        config_commands = [
            [bcdedit_path, '/set', guid, 'device', 'boot'],
            [bcdedit_path, '/set', guid, 'path', '\\'+self.grub_mbr_file],
            [bcdedit_path, '/displayorder', guid, '/addlast']
        ]

        for cmd in config_commands:
            run_shell_cmd(cmd)

        self.mainEngine.config.bcd_guid = guid
        try:
            registry.hSetValue(self.hlmPath, 'BcdeditGUID', guid)
        except:
            log.error('Could not write BCD GUID to registry key.')
        # TODO: enable this after registry errors are fixed. 
        log.debug('bcdedit record created successfully.')
        return True


    def create_cfg_file(self):
        """
        Writes installation configuration to an .ini file with a filename hard
        coded as a propery in this class and places it under config/ folder
        in the installation root."""
        cfg = RawConfigParser()

        cfg.add_section('config')
        cfg.set('config', 'username', self.mainEngine.config.username)
        cfg.set('config', 'password', self.mainEngine.config.password)
        cfg.set('config', 'drive', self.mainEngine.config.drive.DeviceID)
        cfg.set('config', 'size', self.mainEngine.config.size)

        cfg.add_section('installation')
        cfg.set('installation', 'path', self.getInstallationRoot())
        cfg.set('installation', 'registrykey', self.hlmPath)
        cfg.set('installation', 'date', time.ctime())
        cfg.set('installation', 'logfile', self.mainEngine.logfile)
        cfg.set('installation', 'version', self.mainEngine.appversion)
        cfg.set('installation', 'os', self.mainEngine.compatibility.OS.Caption)
        cfg.set('installation', 'osmajorversion', self.mainEngine.compatibility.winMajorVersion())
        cfg.set('installation', 'grubloader', self.grub_loader_file)
        if hasattr(self.mainEngine.config, 'bcd_guid'):
            cfg.set('installation', 'bcdguid', self.mainEngine.config.bcd_guid)

        if hasattr(self.mainEngine.config, 'isoPath'):
            cfg.set('installation', 'source', 'iso')
        elif hasattr(self.mainEngine.config, 'usbDrive'):
            cfg.set('installation', 'source', 'usb')
        elif hasattr(self.mainEngine.config, 'cdDrive'):
            cfg.set('installation', 'source', 'cd')
        else:
            cfg.set('installation', 'source', 'none')

        cfg.add_section('version')
        if self.mainEngine.version:
            cfg.set('version', 'id', self.mainEngine.version.id)
            cfg.set('version', 'name', self.mainEngine.version.name)
            cfg.set('version', 'kernel', self.mainEngine.version.kernel)
            cfg.set('version', 'initrd', self.mainEngine.version.initrd)
            cfg.set('version', 'img', self.mainEngine.version.img)
        else:
            cfg.set('version', 'id', '')
            cfg.set('version', 'name', '')

        destination = os.path.join(self.getInstallationRoot(), 'config', self.cfg_file)

        try:
            with open(destination, 'wb') as file_handle:
                cfg.write(file_handle)
            log.debug('Successfully written into configuration file.')
            return True
        except IOError as e:
            log.error('IOError on writing configuration file: %s' % e)
            return False


    def copy_installer(self):
        """
        Copier installer root i.e. PaW/ folder and its subdirectories
        recursively into PaW/ folder under the installation root. It determines
        root of installer from sys.executable, however if it is Python
        interpreter, it includes 'Python' and we prevent copying Python
        installation to installation dir., in a case-insensitive manner.
        """
        installer_root = os.path.dirname(sys.executable)
        destination = os.path.join(self.getInstallationRoot(), 'PaW')

        try: # do not allow folder containing 'python'
            if installer_root.lower().index('python') > -1:
                log.warning('Installer executable dir contains \'python\'. Will not be copied!')
        except ValueError: # not an error in fact.
            if not copy_folder(installer_root, destination):
                log.error('Could not copy installer to the installation root.')
                return False
            else:
                log.debug('Copied installer/uninstaller successfully.')
                return True


    def copy_log(self):
        """
        Copies installation log from temporary folder to log/ folder under
        installation root.
        """
        source = self.mainEngine.logfile
        destination = os.path.join(self.getInstallationRoot(), 'log')

        try:
            shutil.copy(source, destination)
            log.debug('Copied installation log.')
            return True
        except Exception as e:
            log.error('Could not copy installation log %s: %s' % (source, e))
            return False


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
            log.debug('Extracted from ISO: %s' % file_path)

        return True


    def createDirStructure(self):
        "Creates directory structure on installation drive."
        base = self.getInstallationRoot()

        self.mainEngine.config.installationRoot = base

        dirs = [
            '.',
            'boot',
            'backup',
            'config',
            'log',
            'paw']

        for dir in dirs:
            path = os.path.join(base, dir)
            try:
                os.mkdir(path)
                log.debug('%s created.' % path)
            except OSError:
                log.debug('%s already exists.' % path)

        return True


    def extract_iso_files(self):
        """
        Extracts predefined (hard-coded in this method) files into boot/ folder
        in the installation path. Those files are kernel, initrd and img.
        """
        source = self.mainEngine.config.isoPath
        destination = os.path.abspath(os.path.join(self.getInstallationRoot(), 'boot'))

        if not os.path.isfile(source):
            log.error('Could not locate ISO %s' % source)
            return False

        if self.mainEngine.version:
            files = [
                self.mainEngine.version.kernel, self.mainEngine.version.initrd,
                self.mainEngine.version.img]
        else:
            log.warning('Could not recognize version. Using default CD paths.')
            files = [self.default_kernel_path, self.default_initrd_path,
                self.default_img_path]

        self.extract_from_iso(source, destination, files)
        log.debug('Files extracted from ISO.')
        return True


    def copy_files_from_device(self, isCD = True):
        """
        Copies predefined (hard-coded in this method) files from given
        device into 'boot' folder under installation root.. Those files are
        kernel, initrd and img. If isCD is True, it looks for configured CD
        device; otherwise, USB device will be set as the source.
        """
        source = 'CD' if isCD else 'USB'
        
        log.debug('Start copying files from %s.' % source)
        if isCD:
            device_root = self.mainEngine.config.cdDrive.DeviceID + '\\'
        else:
            device_root = self.mainEngine.config.usbDrive.DeviceID + '\\'
            
        destination = os.path.abspath(os.path.join(self.getInstallationRoot(), 'boot'))

        if self.mainEngine.version:
            files = [
                self.mainEngine.version.kernel, self.mainEngine.version.initrd,
                self.mainEngine.version.img]
        else:
            log.warning('Could not recognize version. Using default %s paths.' % source)
            files = [self.default_kernel_path, self.default_initrd_path,
                self.default_img_path]

        for file_path in files:
            path = os.path.abspath(os.path.join(device_root, file_path))

            if not os.path.isfile(path):
                log.error('Could not locate %s' % path)
                return False

            try:
                shutil.copy(path, destination)
                log.debug('%s copied to %s' % (path, destination))
            except IOError as e:
                log.error('Could not copy: %s' % e); return False
                
        return True


    def copy_cd_files(self):
        return self.copy_files_from_device(isCD = True) # CD.


    def copy_usb_files(self):
        return self.copy_files_from_device(isCD = False) # USB.


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
        menu_lst_dest = os.path.join(destination, self.menu_lst_file)
        template_source = os.path.join(source, self.menu_lst_template_file)
        if not os.path.isfile(template_source):
            # template source may be in the same folder with installer.
            template_source = os.path.abspath(self.menu_lst_template_file)
            
        menu_lst = populate_template_file(template_source, values)
        try:
            menu_lst_stream = open(menu_lst_dest, 'w')
            menu_lst_stream.write(menu_lst)
            menu_lst_stream.close
            log.debug('%s created successfully.' % menu_lst_dest)
        except IOError as e:
            log.error('Could not write %s. %s' % (menu_lst_dest, e))
            return False

        # copy pardus.tag
        tagpath = os.path.abspath(os.path.join(source, self.grub_identifier_file))
        tag_destination = os.path.abspath(self.mainEngine.config.drive.DeviceID + '\\')
        if not os.path.isfile(tagpath):
             # look at the executable folder
            log.error('Could not locate %s, trying for the same folder.' % tagpath)
            tagpath = os.path.abspath(self.grub_identifier_file)

        if not os.path.isfile(tagpath):
            log.error('Could not locate %s' % tagpath)
            return False
        try:
            shutil.copy(tagpath, tag_destination)
            log.debug('%s TAGFILE copied to %s' % (os.path.basename(tagpath), tag_destination))
        except IOError as e:
            log.error('Could not copy tag file %s: %s' % (tagpath,e))
            return False

        # copy rest of grub4dos files
        files = [self.grub_loader_file, self.grub_mbr_file]
        for file_name in files:
            path = os.path.abspath(os.path.join(source, file_name))

            if not os.path.isfile(path):
                log.error('Could not locate %s, trying for the same folder.' % path)
                path = os.path.abspath(file_name) # look at the executable folder

            if not os.path.isfile(path):
                log.error('Could not locate %s' % path)
                return False
            try:
                shutil.copy(path, destination)
                log.debug('%s copied to %s' % (os.path.basename(path), destination))
            except IOError as e:
                log.error('Could not copy grub4dos file %s: %s' % (path,e))
                return False
        return True


    def start(self):
        "Starts installation process specific for ISOs and CD/DVDs."
        self.tasklist = TaskList(callback=self.onAdvance)
        
        if hasattr(self.mainEngine.config, 'isoPath'):
            log.debug('ISO installation is starting...')
            tasks = self.get_iso_installation_tasks(self.tasklist)
        elif hasattr(self.mainEngine.config, 'usbDrive'):
            log.debug('USB installation is starting...')
            tasks = self.get_usb_installation_tasks(self.tasklist)
        elif hasattr(self.mainEngine.config, 'cdDrive'):
            log.debug('CD installation is starting...')
            tasks = self.get_cd_installation_tasks(self.tasklist)
        else:
            log.error('Installation source could not be determined.')

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
            Task(self.copy_installer, 'Copying PaW installer files', cb),
            #Task(self.copy_cd_files, 'Copying files from CD', cb),
            Task(self.copy_grub4dos_files, 'Copying and preparing GRUB files', cb),
            Task(self.installationRegistry, 'Creating Registry keys', cb),
            #Task(self.modify_boot_sequence, 'Modifying Windows boot configuration', cb),
            Task(self.create_cfg_file, 'Creating configuration file', cb),
            Task(self.ejectCD, 'Ejecting CD tray', cb),
            Task(self.copy_log, 'Copying installation log.', cb),
        ]


    def get_usb_installation_tasks(self, associated_tasklist):
        cb = associated_tasklist.startNext # callback

        def foo():pass
        
        return [
            Task(self.createDirStructure, 'Creating directory structure', cb),
            Task(self.copy_installer, 'Copying PaW installer files', cb),
            Task(self.copy_usb_files, 'Copying files from USB', cb),
            Task(self.copy_grub4dos_files, 'Copying and preparing GRUB files', cb),
            Task(self.installationRegistry, 'Creating Registry keys', cb),
            Task(self.modify_boot_sequence, 'Modifying Windows boot configuration', cb),
            Task(self.create_cfg_file, 'Creating configuration file', cb),
            Task(self.copy_log, 'Copying installation log.', cb),
        ]

    def get_iso_installation_tasks(self, associated_tasklist):
        cb = associated_tasklist.startNext # callback

        def foo():pass

        return [
            Task(self.createDirStructure, 'Creating directory structure', cb),
            Task(self.copy_installer, 'Copying PaW installer files', cb),
            Task(self.extract_iso_files, 'Extracting files from ISO', cb),
            Task(self.copy_grub4dos_files, 'Copying and preparing GRUB files', cb),
            Task(self.installationRegistry, 'Creating Registry keys', cb),
            Task(self.modify_boot_sequence, 'Modifying Windows boot configuration', cb),
            Task(self.create_cfg_file, 'Creating configuration file', cb),
            Task(self.copy_log, 'Copying installation log.', cb),
        ]
