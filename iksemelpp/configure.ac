dnl Process this file with autoconf to produce a configure script.

AC_PREREQ(2.50)
AC_INIT
AC_CONFIG_SRCDIR([configure.ac])
dnl Every other copy of the package version number gets its value from here
AM_INIT_AUTOMAKE(iksemelpp,0.1)

dnl create a config.h file (Automake will add -DHAVE_CONFIG_H)
AM_CONFIG_HEADER(include/config.h)

AC_SUBST(VERSION)

ISODATE=`date +%Y-%m-%d`
AC_SUBST(ISODATE)

AC_ARG_ENABLE(gc,
[  --enable-gc           install Garbage Collector support],
)

AC_CANONICAL_HOST

dnl Checks for programs.
AC_PROG_INSTALL
AC_PROG_CC
AC_PROG_CXX
AC_PROG_RANLIB
AM_PROG_LIBTOOL

dnl Checks for libraries.

AM_CONDITIONAL(HAVE_GC, test "${enable_gc}" = yes)

dnl Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS(unistd.h strings.h errno.h)

dnl Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_C_INLINE

dnl Generating makefiles.
AC_CONFIG_FILES([
Makefile
src/Makefile
include/Makefile
examples/Makefile
])
AC_OUTPUT
