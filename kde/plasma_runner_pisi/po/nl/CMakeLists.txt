file(GLOB _po_files LC_MESSAGES/*.po)
GETTEXT_PROCESS_PO_FILES( nl ALL INSTALL_DESTINATION ${LOCALE_INSTALL_DIR} ${_po_files} )
