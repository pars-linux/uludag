PROJECT(kaptan)
FIND_PACKAGE(KDE3 REQUIRED)

# Find xgettext
FIND_PROGRAM(
    XGETTEXT_PATH
    NAMES "xgettext"
    PATHS "/usr/bin"
)
IF(${XGETTEXT_PATH} STREQUAL "XGETTEXT_PATH-NOTFOUND")
    MESSAGE(STATUS "xgettext not found.  You will not be able to run 'make extract_messages' in the 'po' directory.")
ELSE(${XGETTEXT_PATH} STREQUAL "XGETTEXT_PATH-NOTFOUND")
    MESSAGE(STATUS "Found xgettext: ${XGETTEXT_PATH}")
ENDIF(${XGETTEXT_PATH} STREQUAL "XGETTEXT_PATH-NOTFOUND")

# Find extractrc
FIND_PROGRAM(
    EXTRACTRC_PATH
    NAMES "extractrc"
    PATHS "/usr/bin"
)
IF(${EXTRACTRC_PATH} STREQUAL "EXTRACTRC_PATH-NOTFOUND")
    MESSAGE(STATUS "extractrc not found.  You will not be able to run 'make extract_messages' in the 'po' directory.")
ELSE(${EXTRACTRC_PATH} STREQUAL "EXTRACTRC_PATH-NOTFOUND")
    MESSAGE(STATUS "Found extractrc: ${EXTRACTRC_PATH}")
ENDIF(${EXTRACTRC_PATH} STREQUAL "EXTRACTRC_PATH-NOTFOUND")

ADD_SUBDIRECTORY(src)
ADD_SUBDIRECTORY(po)
ADD_SUBDIRECTORY(themes)
