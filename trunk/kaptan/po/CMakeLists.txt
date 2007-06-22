SET(POT_FILE ${CMAKE_CURRENT_BINARY_DIR}/kaptan.pot)

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
INSTALL(FILES ${_gmofile} DESTINATION share/locale/${_lang}/LC_MESSAGES RENAME kaptan.mo)
SET(_gmofiles ${_gmofiles} ${_gmofile})
ENDFOREACH(_po ${PO_FILES})

ADD_CUSTOM_TARGET(translations ALL DEPENDS ${_gmofiles})

# Stuff to generate the .pot
FILE(GLOB POT_UIFILES ../src/*.ui)
SET(POT_SOURCES ../src/*.cpp)
SET(POT_OUTPUT kaptan.pot)

ADD_CUSTOM_COMMAND(
    OUTPUT _${POT_OUTPUT}
    COMMAND ${EXTRACTRC_PATH} ${POT_UIFILES} > rc.cpp
    COMMAND ${XGETTEXT_PATH} --foreign-user -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale -x "${KDE3_INCLUDE_DIR}/kde.pot" -o ${POT_OUTPUT} rc.cpp ${POT_SOURCES}
    COMMAND rm rc.cpp
)

ADD_CUSTOM_TARGET(
    extract_messages
    DEPENDS _${POT_OUTPUT}
)

