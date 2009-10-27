SET(POT_FILE ${CMAKE_CURRENT_BINARY_DIR}/tasma.pot)

SET(
  PO_FILES
  ca.po
  de.po
  es.po
  fr.po
  it.po
  nl.po
  pt_BR.po
  tr.po
  )

SET(_gmofiles)
FOREACH(_po ${PO_FILES})
  GET_FILENAME_COMPONENT(_lang ${_po} NAME_WE)
  SET(_gmofile ${CMAKE_CURRENT_BINARY_DIR}/${_lang}.gmo)
  ADD_CUSTOM_COMMAND(
    OUTPUT ${_gmofile}
    COMMAND msgmerge ARGS --quiet --update --backup=none -s ${CMAKE_CURRENT_SOURCE_DIR}/${_po} ${POT_FILE}
    COMMAND msgfmt ARGS -o ${_gmofile} ${CMAKE_CURRENT_SOURCE_DIR}/${_po}
    DEPENDS ${POT_FILE} ${CMAKE_CURRENT_SOURCE_DIR}/${_po}
  )
INSTALL(FILES ${_gmofile} DESTINATION share/locale/${_lang}/LC_MESSAGES RENAME tasma.mo)
SET(_gmofiles ${_gmofiles} ${_gmofile})
ENDFOREACH(_po ${PO_FILES})

ADD_CUSTOM_TARGET(translations ALL DEPENDS ${_gmofiles})
