find_package(KDE4 REQUIRED)
include_directories(${KDE4_INCLUDES})

set(knazar_SRCS
main.cpp
)

kde4_add_executable(knazar ${knazar_SRCS})
target_link_libraries(knazar ${KDE4_KDEUI_LIBS})
