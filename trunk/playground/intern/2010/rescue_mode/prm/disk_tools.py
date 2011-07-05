# -*- coding: utf-8 -*-
import glob
import os
from pardus import diskutils
import comar
import parted
from shell_tools import run_quiet
#from shutil import rmtree
#import time

MOUNTED_PARDUS = set([])

def get_device_model(devices):
    devices_model = []
    for i in devices:
        device_name = parted.PedDevice.get(i[1]).model
        devices_model.append([device_name, i])
    return devices_model

def get_partitions_labels():
    partitions_labels = set([])

    for i in glob.glob("/dev/disk/by-label/*"):
        partitions_labels.add(i.lstrip("/dev/disk/by-label/"))
    return partitions_labels

def get_pardus_partitions():
    pardus_partitions = []

    for i in get_partitions_labels():
        if "PARDUS_ROOT" in i:
            i = [i, diskutils.getDeviceByLabel(i)]
        pardus_partitions.append(i)
    return pardus_partitions

def get_pardus_part_info():
    pardus_part_info = []
    link = comar.Link(socket="/var/run/dbus/system_bus_socket")

    for i in get_pardus_partitions():
        path = "/mnt/rescue_disk/"+i[0]

        MOUNTED_PARDUS.add(path)
        if os.path.exists(path):
            flag = True
            for mounted in link.Disk.Manager["mudur"].getMounted():
                if str(mounted[1]) == path:
                    flag = False
                    if str(mounted[0]) != i[1] :
                        link.Disk.Manager["mudur"].umount(path)
                        link.Disk.Manager["mudur"].mount(i[1], path)
            if flag:
                link.Disk.Manager["mudur"].mount(i[1], path)
        else:
            os.makedirs(path)
            link.Disk.Manager["mudur"].mount(i[1], path)
        pardus_part_info.append([
          open(path+"/etc/pardus-release").read().rstrip("\n"),
            i[1], i[0], path])

    return pardus_part_info


def get_windows_partitions():

    windows_partitions = []
    device_list = diskutils.getDeviceMap()

    for i in device_list:
        device = parted.PedDevice.get(i[1])
        disk = parted.PedDisk.new(device)
        path = disk.next_partition()
        while path:
            if path.fs_type:
                if path.fs_type.name in ("ntfs", "fat32"):
                    if is_windows("%s%d" % (i[1], path.num), path.fs_type.name):
                        windows_partitions.append([i[1], path.num,
                          path.fs_type.name, "%s%d" % (i[1], path.num)])
            path = disk.next_partition(path)

    return windows_partitions

def is_windows(partition_path, file_system):
    m_dir = "/tmp/_pcheck"
    if not os.path.isdir(m_dir):
        os.makedirs(m_dir)
    umount(m_dir)
    try:
        if file_system == "fat32":
            mount(partition_path, m_dir, "vfat")
        else:
            mount(partition_path, m_dir, file_system)
    except:
        return False

    exist = lambda f: os.path.exists(os.path.join(m_dir, f))

    if exist("boot.ini") or exist("command.com") or exist("bootmgr"):
        umount(m_dir)
        return True
    else:
        umount(m_dir)
        return False

def umount_pardus():
    link = comar.Link(socket="/var/run/dbus/system_bus_socket")
    for i in MOUNTED_PARDUS:
        while True:
            try:
                link.Disk.Manager["mudur"].umount(i)
                break
            except comar.dbus.DBusException:
                pass

def mount(source, target, file_system):
    run_quiet("mount -t %s %s %s" % (file_system, source, target))
def umount(target):
    run_quiet("umount %s" % (target))



#def main():
 # link = comar.Link(socket="/var/run/dbus/system_bus_socket")
  #link.Disk.Manager["mudur"].umount("/mnt/rescue_disk/PARDUS_ROOT1")
  

#if __name__=="__main__":
#  main()
    

  
  

  
