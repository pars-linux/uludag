#!/usr/bin/python
# -*- coding: utf-8 -*-
import yali
import yali.context as ctx
from devicemapper import DeviceMapper
from device import DeviceError
from yali.storage.library import lvm
from yali.baseudev import udev_settle
from yali.storage.library import devicemapper

class LogicalVolumeError(yali.Error):
    pass

class LogicalVolume(DeviceMapper):
    """ An LVM Logical Volume """
    _type = "lvmlv"
    _resizable = True
    _packages = ["lvm2"]

    def __init__(self, name, vgdev, size=None, uuid=None,
                 stripes=1, logSize=0, snapshotSpace=0,
                 format=None, exists=None, sysfsPath='',
                 grow=None, maxsize=None, percent=None):
        """ Create a LogicalVolume instance.

            Arguments:

                name -- the device name (generally a device node's basename)
                vgdev -- volume group (LVMVolumeGroupDevice instance)

            Keyword Arguments:

                size -- the device's size (in MB)
                uuid -- the device's UUID
                stripes -- number of copies in the vg (>1 for mirrored lvs)
                logSize -- size of log volume (for mirrored lvs)
                snapshotSpace -- sum of sizes of snapshots of this lv
                sysfsPath -- sysfs device path
                format -- a DeviceFormat instance
                exists -- indicates whether this is an existing device

                For new (non-existent) LVs only:

                    grow -- whether to grow this LV
                    maxsize -- maximum size for growable LV (in MB)
                    percent -- percent of VG space to take

        """
        if isinstance(vgdev, list):
            if len(vgdev) != 1:
                raise ValueError("constructor requires a single LVMVolumeGroupDevice instance")
            elif not isinstance(vgdev[0], LVMVolumeGroupDevice):
                raise ValueError("constructor requires a LVMVolumeGroupDevice instance")
        elif not isinstance(vgdev, LVMVolumeGroupDevice):
            raise ValueError("constructor requires a LVMVolumeGroupDevice instance")

        DeviceMapper.__init__(self, name, size=size, format=format,
                              sysfsPath=sysfsPath, parents=vgdev, exists=exists)

        self.uuid = uuid
        self.snapshotSpace = snapshotSpace
        self.stripes = stripes
        self.logSize = logSize

        self.req_grow = None
        self.req_max_size = 0
        self.req_size = 0   
        self.req_percent = 0

        if not self.exists:
            self.req_grow = grow
            self.req_max_size = numeric_type(maxsize)
            # XXX should we enforce that req_size be pe-aligned?
            self.req_size = self._size
            self.req_percent = numeric_type(percent)

        # here we go with the circular references
        self.vg._addLogVol(self)

    def __str__(self):
        s = DeviceMapper.__str__(self)
        s += ("  VG device = %(vgdev)r  percent = %(percent)s\n"
              "  mirrored = %(mirrored)s stripes = %(stripes)d"
              "  snapshot total =  %(snapshots)dMB\n"
              "  VG space used = %(vgspace)dMB" %
              {"vgdev": self.vg, "percent": self.req_percent,
               "mirrored": self.mirrored, "stripes": self.stripes,
               "snapshots": self.snapshotSpace, "vgspace": self.vgSpaceUsed })
        return s

    @property
    def dict(self):
        d = super(LogicalVolume, self).dict
        if self.exists:
            d.update({"mirrored": self.mirrored, "stripes": self.stripes,
                      "snapshots": self.snapshotSpace,
                      "vgspace": self.vgSpaceUsed})
        else:
            d.update({"percent": self.req_percent})

        return d

    @property
    def mirrored(self):
        return self.stripes > 1

    def _setSize(self, size):
        size = self.vg.align(numeric_type(size))
        ctx.logger.debug("trying to set lv %s size to %dMB" % (self.name, size))
        if size <= (self.vg.freeSpace + self._size):
            self._size = size
            self.targetSize = size
        else:
            ctx.logger.debug("failed to set size: %dMB short" % (size - (self.vg.freeSpace + self._size),))
            raise ValueError("not enough free space in volume group")

    size = property(StorageDevice._getSize, _setSize)

    @property
    def vgSpaceUsed(self):
        return self.size * self.stripes + self.logSize + self.snapshotSpace

    @property
    def vg(self):
        """ This Logical Volume's Volume Group. """
        return self.parents[0]

    @property
    def mapName(self):
        """ This device's device-mapper map name """
        # Thank you lvm for this lovely hack.
        return "%s-%s" % (self.vg.mapName, self._name.replace("-","--"))

    @property
    def path(self):
        """ Device node representing this device. """
        return "%s/%s" % (self._devDir, self.mapName)

    def getDMNode(self):
        """ Return the dm-X (eg: dm-0) device node for this device. """
        if not self.exists:
            raise DeviceError("device has not been created", self.name)

        return devimapper.dm_node_from_name(self.mapName)

    @property
    def name(self):
        """ This device's name. """
        return "%s-%s" % (self.vg.name, self._name)

    @property
    def lvname(self):
        """ The LV's name (not including VG name). """
        return self._name

    @property
    def complete(self):
        """ Test if vg exits and if it has all pvs. """
        return self.vg.complete

    def setup(self, intf=None, orig=False):
        """ Open, or set up, a device. """
        if not self.exists:
            raise DeviceError("device has not been created", self.name)

        if self.status:
            return

        self.vg.setup(orig=orig)
        lvm.lvactivate(self.vg.name, self._name)

        # we always probe since the device may not be set up when we want
        # information about it
        self._size = self.currentSize

    def teardown(self, recursive=None):
        """ Close, or tear down, a device. """
        if not self.exists and not recursive:
            raise DeviceError("device has not been created", self.name)

        if self.status:
            if self.originalFormat.exists:
                self.originalFormat.teardown()
            if self.format.exists:
                self.format.teardown()
            udev_settle()

        if self.status:
            lvm.lvdeactivate(self.vg.name, self._name)

        if recursive:
            # It's likely that teardown of a VG will fail due to other
            # LVs being active (filesystems mounted, &c), so don't let
            # it bring everything down.
            try:
                self.vg.teardown(recursive=recursive)
            except Exception as e:
                ctx.logger.debug("vg %s teardown failed; continuing" % self.vg.name)

    def create(self):
        """ Create the device. """
        if self.exists:
            raise DeviceError("device already exists", self.name)
        try:
            self.createParents()
            self.setupParents()

            # should we use --zero for safety's sake?
            lvm.lvcreate(self.vg.name, self._name, self.size, progress=w)
        except Exception:
            raise
        else:
            # FIXME set / update self.uuid here
            self.exists = True
            self.setup()

    def destroy(self):
        """ Destroy the device. """
        if not self.exists:
            raise DeviceError("device has not been created", self.name)

        self.teardown()
        # set up the vg's pvs so lvm can remove the lv
        self.vg.setupParents(orig=True)
        lvm.lvremove(self.vg.name, self._name)
        self.exists = False

    def resize(self):
        # XXX resize format probably, right?
        if not self.exists:
            raise DeviceError("device has not been created", self.name)

        # Setup VG parents (in case they are dmraid partitions for example)
        self.vg.setupParents(orig=True)

        if self.originalFormat.exists:
            self.originalFormat.teardown()
        if self.format.exists:
            self.format.teardown()

        udev_settle()
        lvm.lvresize(self.vg.name, self._name, self.size)
