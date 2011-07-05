# -*- coding: utf-8 -*-
"""TÜBİTAK UEKAE 2010 
   Author: Mehmet Burak Aktürk 
   E-mail: mb.akturk@gmail.com"""
import urwid
import time
import disk_tools
import gui_tools
import dbus_tools
import bootloader_tools
from shell_tools import reboot
from shell_tools import shutdown
from pardus import diskutils
import gc
import os

class RescueMode:
    """This class for using to rescue pardus system
    and Windows bootloader"""
    palette = [('window', 'black', 'light gray'),
         ('focus', 'white', 'dark red'),
         ('border', 'black', 'dark blue'),
         ('p_border', 'black', 'light gray'),
         ('shadow', 'white', 'black'),
         ('body', 'black', 'dark blue')]

    def __init__(self):
        self.screen_container = []
        self.other_inputs = None
        self.dbus = None
        self.selected_disk = None
        self.pardus_device = None
        self.loop = None
        self.boot_device = None
        self.selected_disk_info = None
        self.other_devices = None

        self.popup_status = -1

        #create main frame
        body = urwid.Filler(urwid.Divider(),'top')
        header = urwid.AttrWrap(urwid.Padding(
            urwid.Text("PRM - Pardus Rescue Mode"),'center'),'window')
        footer = urwid.AttrWrap(
            urwid.Padding(urwid.Text("< UP - DOWN > Move on menu | "+
                "< ENTER > Select | < ESC > Cancel or Back | <F1> About PRM | "+
                "<F10>  Quit"),'right'),'window')
        self.main_frame = urwid.Frame(body, header, footer)


        #call first screen method
        self.ro_screen()

    def ro_screen(self, forward=True):
        """ro_screen = rescue options screen
        this method shows rescue options to user"""
        #create firt window
        self.disconnect_dbus()
        frame = gui_tools.ListDialog(None, ['window', 'focus'],
                "Please select an option from list")
        frame.add_item("Rescue Pardus", self.sd_screen)
        frame.add_item("Rescue Windows bootloader", self.wl_screen)
        #frame.add_item("Shell'e git",self.go_shell)
        self.create_window(frame, 80, 15)

    def go_shell(self):
        """This method closes the rescue mode and turn the shell"""
        self.pop_up("Unmounting partitions")
        self.close_process()

        self.loop.screen.stop()
        raise urwid.ExitMainLoop()
        

#######################################
######## WINDOWS PROCESS ##############
#######################################

    def wl_screen(self, forward=True):
        """wl_screen = windows list screen
        this method shows windows installed disks
        otherwise shows "there is no windows" message"""
        if forward:
            self.screen_container.append(self.ro_screen)

        def install_win_bl(windows):
            """install_win_bl = install windows
            bootloader"""
            self.pop_up("Rescuing Windows bootloader")
            bootloader_tools.install_windows_bootloader(windows)
            time.sleep(1)
            self.final_screen("Windows bootloader was rescued")

        def windows_info(windows):
            """This method shows the selected windows info in 
               ListDialog footer"""
            return "Selected Windows disk %s file system: %s"\
                        % (windows.args[3], windows.args[2])

        #show info to user by pop up
        self.pop_up("Searching Windows installed disks")
        windows_partitions = disk_tools.get_windows_partitions()

        if windows_partitions:
            frame = gui_tools.ListDialog(windows_info, ['window', 'focus'],
                    "Please select a Windows installed " +
                            "disk which you want to rescue")
            for windows in disk_tools.get_windows_partitions():
                frame.add_item("Windows%s" % windows[1],
                                install_win_bl, windows)
            self.create_window(frame, 80, 15)
        else:
            self.final_screen("There is no Windows installed disk")
        #close pop up and show wl_screen
        #buraya dön dostum
        self.close_popup()

    def sd_screen(self, forward=True):
        """sd_screen = select disk screen
        this method shows installed pardus disks to
        user rescue otherwise shows "there is no pardus
        installed" message"""

        self.disconnect_dbus()
        if forward:
            self.screen_container.append(self.ro_screen)

        def disk_info(disk):
            return "Selected Pardus disk : "+disk.args[0]+" label:"+disk.args[1]

        def select_disk(disk):
            self.selected_disk = disk
            self.pardus_device = diskutils.parseLinuxDevice(disk[0])
            self.other_devices = diskutils.getDeviceMap()
            self.selected_disk_info = "Selected Pardus disk : %s label: %s "\
                   % (self.selected_disk[0],self.selected_disk[1])
            self.sop_screen()

        pardus_partitions = disk_tools.get_pardus_part_info()

        if pardus_partitions:
            frame = gui_tools.ListDialog(disk_info, ['window', 'focus'],
                    "Please select a partition from list")

            for pardus in disk_tools.get_pardus_part_info():
                frame.add_item(pardus[0], select_disk,
                        [pardus[1], pardus[2], pardus[3]])

            self.create_window(frame, 80, 15)
        else:
            self.final_screen("There is no Pardus installed disk")

    def sop_screen(self, forward=True):
        """sop_screen = select operation screen
        this method shows rescue operation 
        about selected pardus partition"""
        if forward:
            self.screen_container.append(self.sd_screen)

        frame = gui_tools.ListDialog(self.selected_disk_info,
         ['window', 'focus'], "Please select an operation")

        frame.add_item("Reinstall GRUB (boot problems)", 
                       self.go_screen)
        frame.add_item("Change password (lost password)", self.ul_screen)
        frame.add_item("Pisi history (undo package operations)",
                       self.phl_screen)

        self.create_window(frame, 80, 15)

#######################################
######## GRUB PROCESS #################
#######################################

    def go_screen(self, forward=True):
        """go_screen == grub operation screen
        this method shows grub operations"""

        if forward:
            self.screen_container.append(self.sop_screen)

        frame = gui_tools.ListDialog(self.selected_disk_info,
        ['window','focus'],"Please select target to install bootloader")

        screen = self.install_grub
        if len(self.other_devices)>1:
            screen = self.select_grub_disk
        frame.add_item("Firt bootable disk (recommended)", screen, 0)
        frame.add_item("Pardus installed partition", self.install_grub, 1)

        self.create_window(frame, 80, 15)

    def select_grub_disk(self, args):
        self.screen_container.append(self.go_screen)

        def disk_info(disk):
            return "Selected disk : "+disk.args[0][1]

        def install_grub(args):
            self.boot_device = args[0][0]
            self.install_grub(args[1])

        frame = gui_tools.ListDialog(disk_info, ['window', 'focus'],
                "There are more then one bootable disk. Please" +
                    " select a disk from list to install bootloader")

        for i in disk_tools.get_device_model(self.other_devices):
            frame.add_item(i[0], install_grub, [i[1], 2])

        self.create_window(frame, 90, 15)

    def install_grub(self, option):
        if option == 2:
            bootloader_tools.install_grub([self.pardus_device[2],
                    self.pardus_device[3], self.boot_device], option)
        else:
            bootloader_tools.install_grub([self.pardus_device[2],
                    self.pardus_device[3]], option)
        self.pop_up("Installing bootloader ")
        time.sleep(1)
        self.final_screen("Bootloader was installed")


#######################################
######## PASSWORD PROCESS #############
#######################################

    def ul_screen(self, forward=True):
        """ul_screen = userlist screen
        this method shows user list from user
        selected pardus partition"""

        if forward:
            self.screen_container.append(self.sop_screen)
        self.connect_dbus()
        self.pop_up("Getting user list")
        users = self.dbus.get_userlist()
        frame = gui_tools.ListDialog(self.selected_disk_info,
            ['window', 'focus'], "Please select an user")


        for user in users:
            frame.add_item(str(user[1] + " (%s)"
                    % str(user[2])), self.change_password, user)

        self.create_window(frame, 80, 30)
        self.close_popup()

    def change_password(self, user):
        self.screen_container.append(self.ul_screen)

        def error_message(message):
            frame.clear_boxes()
            self.pop_up(message)
            time.sleep(2)
            self.close_popup()

        def func(passwd, re_passwd):
            if passwd == re_passwd:
                if passwd != "" :
                    self.pop_up("Password was updating")
                    time.sleep(1)
                    return_value = self.dbus.set_userpass(int(user[0]), passwd)
                    if return_value[0] == 'message':
                        self.final_screen(return_value[1])
                    else:
                        error_message(return_value[1])
            else:
                error_message("Passwords do not match")

        edit_captions = ["New password         :",
                        "New password (again) :"]

        frame = gui_tools.PasswordDialog(func, 
                ['window', 'focus'], edit_captions, 
                    "The user whose password will be update: %s " % user[1])


        self.other_inputs = frame.unhandled_input
        self.create_window(frame, 80, 15)


#######################################
######## PISI HISTORY #################
#######################################

    def phl_screen(self, forward=True):
        """phl_Screen = pisi history list screen
        this method shows pisi history from user selected
        pardus partitions"""

        if forward:
            self.screen_container.append(self.sop_screen)
        self.connect_dbus()

        self.pop_up("Getting Pisi history information")
        historys = self.dbus.get_history()
        frame = gui_tools.ListDialog(self.selected_disk_info,
            ['window', 'focus'], "Please select an operation to undo")

        for history in historys:
            frame.add_item("operation: %d, %s (%s)" % 
                    (history.no, history.date, history.type),
                        self.phal_screen, history.no)

        self.create_window(frame, 80, 30)
        self.close_popup()

    def phal_screen(self, number):
        """phal_screen = pisi history actions list
        screen. This method showss actions list which will
        be done after user select a history from history list"""

        def take_back():
            self.pop_up("Taking back Pisi history")
            self.dbus.take_back(number)
            self.final_screen("Pisi history was taken back")
            self.close_popup()

        history_dic = self.dbus.get_history_actions(number)
        frame = gui_tools.ListDialog("Please press ENTER if you want to"+
                " continue or press ESC to cancel",
                    ['focus', 'window'], "There are %d actions" %
                        len(history_dic))

        counter = 1
        for i in history_dic:
            frame.add_item("action %d : %s %s" %
                    (counter,history_dic[i][0],i),take_back)
            counter += 1

        window = gui_tools.create_window(frame, ["focus", "p_border", "shadow"])
        widget = urwid.Overlay(window, self.main_frame, 
                'center', 60, 'middle', 20)
        self.loop.widget = widget
        self.loop.draw_screen()
        self.popup_status = 0

    def final_screen(self, message):
        self.screen_container = [self.ro_screen]
        body = urwid.Padding(urwid.Text(message+" Press ESC to return main "+
               "menu or press F10 to quit"), 'center')
        body = urwid.Filler(body, 'middle')
        self.create_window(body, 80, 15)
        self.close_popup()
        self.other_inputs = None

    def about_rescuemode(self):
        self.pop_up("Pardus Rescue Mode\n\nVersion:1.0 (beta)\n"+
                    "Licence:GPL_v2\n\n" +
                    "Author:Mehmet Burak Aktürk\n"+
                    "E-mail: mb.akturk@gmail.com", height=10, status=0)

    def create_window(self, body, width, height):
        window = gui_tools.create_window(body, ["window", "border", "shadow"])
        window = urwid.Padding(window, 'center', width )
        window = urwid.Filler(window, 'middle', height )
        self.main_frame.body = urwid.AttrWrap(window, 'body')
        gc.collect()



    def close_screen(self):
        def reboot_sys():
            self.close_process()
            reboot()
        def shutdown_sys():
            self.close_process()
            shutdown()
            
        self.close_popup()
        frame = gui_tools.ListDialog(None,
                ['focus', 'window'], "Please select what you want to do")
        frame.add_item("Go to shell", self.go_shell)
        frame.add_item("Restart Computer",reboot_sys)
        frame.add_item("Shut down", shutdown_sys)

        window = gui_tools.create_window(frame, ["focus", "p_border", "shadow"])
        widget = urwid.Overlay(window, self.main_frame,
                'center', 50,'middle', 10)
        self.loop.widget = widget
        self.loop.draw_screen()
        self.popup_status = 0

    def pop_up(self, message, width=50, height=5, status=1):
        self.close_popup()
        window = gui_tools.create_window(urwid.Filler(
            urwid.Padding(urwid.Text(message), 'center'), 'top'),
                ["focus", "p_border", "shadow"])
        widget = urwid.Overlay(window, self.main_frame,
                'center',width, 'middle', height)
        self.loop.widget = widget
        self.loop.draw_screen()
        self.popup_status = status

    def close_popup(self):
        self.popup_status = -1
        self.loop.widget = self.main_frame

    def connect_dbus(self):
        if self.dbus == None or self.dbus.path != self.selected_disk[2]:
            self.pop_up("Trying to connect DBus")
            self.dbus = dbus_tools.PardusDbus(self.selected_disk[2])

    def disconnect_dbus(self):
        if self.dbus != None:
            self.pop_up("Trying to disconnect DBus")
            self.dbus.finalize_chroot()
            self.dbus = None
            self.close_popup()

    def close_process(self):
        self.disconnect_dbus()
        disk_tools.umount_pardus()

    def run(self):
        """This metod executes rescue_mode program"""
        self.loop = urwid.MainLoop(self.main_frame,
                self.palette, unhandled_input=self.io_handler)
        self.loop.screen.tty_signal_keys('undefined',
                'undefined', 'undefined', 'undefined', 'undefined')
        self.loop.screen.start()
        self.loop.run()

    def io_handler(self, pressed):
        if 'f1'in pressed :
            self.about_rescuemode()
        if 'esc' in pressed:
            if self.popup_status == 0:
                self.close_popup()
            elif self.popup_status == 1:
                pass
            elif self.popup_status == -1:
                if self.screen_container:
                    self.screen_container.pop()(False)
        if 'f10' in pressed:
            self.close_screen()

        if self.other_inputs:
            self.other_inputs(pressed)


    