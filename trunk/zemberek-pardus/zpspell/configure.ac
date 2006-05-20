AC_INIT
AM_INIT_AUTOMAKE(zpspell,0.3)
AM_CONFIG_HEADER(config.h)

dnl C++ program
AC_PROG_CXX
AC_PROG_INSTALL
AC_LANG_CPLUSPLUS
AC_HEADER_STDC
AC_CHECK_HEADERS(iostream string sstream vector algorithm,,exit)
AC_CHECK_HEADERS(sys/types.h sys/socket.h netinet/in.h netdb.h,,exit)

AC_CONFIG_FILES([ Makefile ])
AC_OUTPUT
