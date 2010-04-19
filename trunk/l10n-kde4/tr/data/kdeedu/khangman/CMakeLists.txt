FILE(GLOB datafiles *.kvtml)
install( FILES ${datafiles} DESTINATION  ${DATA_INSTALL_DIR}/kvtml/tr)
install( FILES  tr.txt  DESTINATION ${DATA_INSTALL_DIR}/khangman )
