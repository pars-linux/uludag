CC = gcc
CFLAGS = -g -Wall

LIBCURSES := -lncurses -lmenu

TARGETS = pxebootselect

INITRAMFS = ` ls /boot | sort -r | grep -m 1 initramfs- `
VERSION = ` ls /boot | sort -r | grep -m 1 initramfs- | cut -c11- `
KERNEL = kernel-$(VERSION)
TFTPBOOT_PATH = /tftpboot/pts/latest-ptsp

all:
	$(CC) $(CFLAGS) `xml2-config --cflags` client/pxe_select_boot/pxebootselect.c -o $(TARGETS) $(LIBCURSES) `xml2-config --libs`

clean:
	rm -f /lib/initramfs/$(TARGETS)
	rm -f /opt/ptsp/pxeboot_iso_files.xml
	rm -rf $(TFTPBOOT_PATH)
	rm -rf /tftpboot/pts/$(VERSION)-ptsp
	
install:
	python server/iso_to_xml.py /opt/ptsp
	
	cp client/initramfs/init /lib/initramfs
	cp client/pxe_select_boot/pxebootselect /lib/initramfs

	mkdir /tftpboot/pts/$(VERSION)-ptsp
	rm -rf $(TFTPBOOT_PATH)
	ln -s $(VERSION)-ptsp $(TFTPBOOT_PATH)

	python client/initramfs/mkinitramfs -o $(TFTPBOOT_PATH) --pxeboot --network -k $(VERSION)

	cp /boot/$(KERNEL) $(TFTPBOOT_PATH)
	mkdir $(TFTPBOOT_PATH)/pxelinux.cfg
	cp pxelinux/pxelinux.cfg/default $(TFTPBOOT_PATH)/pxelinux.cfg/
	cp pxelinux/pxelinux.0 $(TFTPBOOT_PATH)

	cd $(TFTPBOOT_PATH) 
	ln -s $(KERNEL) $(TFTPBOOT_PATH)/latestkernel
	ln -s $(INITRAMFS) $(TFTPBOOT_PATH)/latestinitramfs
