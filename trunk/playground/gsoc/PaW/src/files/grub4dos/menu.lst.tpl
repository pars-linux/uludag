color blue/green yellow/red white/magenta white/magenta
timeout {TIMEOUT}
hiddenmenu
default /default

title {DISTRO}
find --set-root {IDENTIFIER_PATH}
chainloader +1 
kernel {PATH_KERNEL} {KERNEL_PARAMS}
initrd {PATH_INITRD}