# Process this file with autoconf to produce a configure script.
AC_INIT(daemon/autorun.c)
AM_INIT_AUTOMAKE(autorun, 0.1)

# Checks for programs.
AC_PROG_CC
AM_PROG_LEX
AC_PROG_INSTALL
AM_PROG_LIBTOOL
AC_PROG_MAKE_SET
AM_SANITY_CHECK
AM_CONFIG_HEADER(config.h)

# Checks for libraries.
AC_CHECK_LIB(dl,dlopen,ac_dl_lib=0, ac_dl_lib=1)

# Checks for header files.
AC_CHECK_HEADERS([sys/ioctl.h unistd.h])
AC_CHECK_HEADERS(linux/cdrom.h)

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST

# Checks for library functions.

AC_OUTPUT(Makefile daemon/Makefile modules/Makefile modules/cdrom/Makefile)
