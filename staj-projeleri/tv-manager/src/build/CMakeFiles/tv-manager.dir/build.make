# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.6

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canoncical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The program to use to edit the cache.
CMAKE_EDIT_COMMAND = /usr/bin/ccmake

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build

# Include any dependencies generated for this target.
include CMakeFiles/tv-manager.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/tv-manager.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/tv-manager.dir/flags.make

CMakeFiles/tv-manager.dir/main.o: CMakeFiles/tv-manager.dir/flags.make
CMakeFiles/tv-manager.dir/main.o: ../main.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/tv-manager.dir/main.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/tv-manager.dir/main.o -c /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/main.cpp

CMakeFiles/tv-manager.dir/main.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tv-manager.dir/main.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/main.cpp > CMakeFiles/tv-manager.dir/main.i

CMakeFiles/tv-manager.dir/main.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tv-manager.dir/main.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/main.cpp -o CMakeFiles/tv-manager.dir/main.s

CMakeFiles/tv-manager.dir/main.o.requires:
.PHONY : CMakeFiles/tv-manager.dir/main.o.requires

CMakeFiles/tv-manager.dir/main.o.provides: CMakeFiles/tv-manager.dir/main.o.requires
	$(MAKE) -f CMakeFiles/tv-manager.dir/build.make CMakeFiles/tv-manager.dir/main.o.provides.build
.PHONY : CMakeFiles/tv-manager.dir/main.o.provides

CMakeFiles/tv-manager.dir/main.o.provides.build: CMakeFiles/tv-manager.dir/main.o
.PHONY : CMakeFiles/tv-manager.dir/main.o.provides.build

CMakeFiles/tv-manager.dir/tvconfig.o: CMakeFiles/tv-manager.dir/flags.make
CMakeFiles/tv-manager.dir/tvconfig.o: ../tvconfig.cpp
CMakeFiles/tv-manager.dir/tvconfig.o: tvconfig.moc
	$(CMAKE_COMMAND) -E cmake_progress_report /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/tv-manager.dir/tvconfig.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/tv-manager.dir/tvconfig.o -c /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tvconfig.cpp

CMakeFiles/tv-manager.dir/tvconfig.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tv-manager.dir/tvconfig.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tvconfig.cpp > CMakeFiles/tv-manager.dir/tvconfig.i

CMakeFiles/tv-manager.dir/tvconfig.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tv-manager.dir/tvconfig.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tvconfig.cpp -o CMakeFiles/tv-manager.dir/tvconfig.s

CMakeFiles/tv-manager.dir/tvconfig.o.requires:
.PHONY : CMakeFiles/tv-manager.dir/tvconfig.o.requires

CMakeFiles/tv-manager.dir/tvconfig.o.provides: CMakeFiles/tv-manager.dir/tvconfig.o.requires
	$(MAKE) -f CMakeFiles/tv-manager.dir/build.make CMakeFiles/tv-manager.dir/tvconfig.o.provides.build
.PHONY : CMakeFiles/tv-manager.dir/tvconfig.o.provides

CMakeFiles/tv-manager.dir/tvconfig.o.provides.build: CMakeFiles/tv-manager.dir/tvconfig.o
.PHONY : CMakeFiles/tv-manager.dir/tvconfig.o.provides.build

CMakeFiles/tv-manager.dir/tvconfigui.o: CMakeFiles/tv-manager.dir/flags.make
CMakeFiles/tv-manager.dir/tvconfigui.o: ../tvconfigui.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/tv-manager.dir/tvconfigui.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/tv-manager.dir/tvconfigui.o -c /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tvconfigui.cpp

CMakeFiles/tv-manager.dir/tvconfigui.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tv-manager.dir/tvconfigui.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tvconfigui.cpp > CMakeFiles/tv-manager.dir/tvconfigui.i

CMakeFiles/tv-manager.dir/tvconfigui.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tv-manager.dir/tvconfigui.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tvconfigui.cpp -o CMakeFiles/tv-manager.dir/tvconfigui.s

CMakeFiles/tv-manager.dir/tvconfigui.o.requires:
.PHONY : CMakeFiles/tv-manager.dir/tvconfigui.o.requires

CMakeFiles/tv-manager.dir/tvconfigui.o.provides: CMakeFiles/tv-manager.dir/tvconfigui.o.requires
	$(MAKE) -f CMakeFiles/tv-manager.dir/build.make CMakeFiles/tv-manager.dir/tvconfigui.o.provides.build
.PHONY : CMakeFiles/tv-manager.dir/tvconfigui.o.provides

CMakeFiles/tv-manager.dir/tvconfigui.o.provides.build: CMakeFiles/tv-manager.dir/tvconfigui.o
.PHONY : CMakeFiles/tv-manager.dir/tvconfigui.o.provides.build

CMakeFiles/tv-manager.dir/tv-manager.o: CMakeFiles/tv-manager.dir/flags.make
CMakeFiles/tv-manager.dir/tv-manager.o: ../tv-manager.cpp
CMakeFiles/tv-manager.dir/tv-manager.o: tv-manager.moc
	$(CMAKE_COMMAND) -E cmake_progress_report /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/CMakeFiles $(CMAKE_PROGRESS_4)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/tv-manager.dir/tv-manager.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/tv-manager.dir/tv-manager.o -c /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tv-manager.cpp

CMakeFiles/tv-manager.dir/tv-manager.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tv-manager.dir/tv-manager.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tv-manager.cpp > CMakeFiles/tv-manager.dir/tv-manager.i

CMakeFiles/tv-manager.dir/tv-manager.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tv-manager.dir/tv-manager.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tv-manager.cpp -o CMakeFiles/tv-manager.dir/tv-manager.s

CMakeFiles/tv-manager.dir/tv-manager.o.requires:
.PHONY : CMakeFiles/tv-manager.dir/tv-manager.o.requires

CMakeFiles/tv-manager.dir/tv-manager.o.provides: CMakeFiles/tv-manager.dir/tv-manager.o.requires
	$(MAKE) -f CMakeFiles/tv-manager.dir/build.make CMakeFiles/tv-manager.dir/tv-manager.o.provides.build
.PHONY : CMakeFiles/tv-manager.dir/tv-manager.o.provides

CMakeFiles/tv-manager.dir/tv-manager.o.provides.build: CMakeFiles/tv-manager.dir/tv-manager.o
.PHONY : CMakeFiles/tv-manager.dir/tv-manager.o.provides.build

tvconfig.moc: ../tvconfig.h
	$(CMAKE_COMMAND) -E cmake_progress_report /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/CMakeFiles $(CMAKE_PROGRESS_5)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating tvconfig.moc"
	/usr/qt/4/bin/moc -I/usr/qt/4/include -I/usr/qt/4/include/QtGui -I/usr/qt/4/include/QtXml -I/usr/qt/4/include/QtCore -I/usr/qt/4/include/QtXmlPatterns -I/usr/qt/4/include/QtWebKit -I/usr/qt/4/include/QtHelp -I/usr/qt/4/include/QtAssistant -I/usr/qt/4/include/QtDBus -I/usr/qt/4/include/QtTest -I/usr/qt/4/include/QtUiTools -I/usr/qt/4/include/QtScript -I/usr/qt/4/include/QtSvg -I/usr/qt/4/include/QtSql -I/usr/qt/4/include/QtOpenGL -I/usr/qt/4/include/QtNetwork -I/usr/qt/4/include/QtDesigner -I/usr/qt/4/include/Qt3Support -I/usr/qt/4/mkspecs/default -I/home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/-DQT_DLL -I/usr/kde/4/include -I/usr/kde/4/include/KDE -I/usr/qt/4/include/KDE -I/home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build -I/usr/include/pci -D_BSD_SOURCE -DQT_DLL -DQT_GUI_LIB -DQT_XML_LIB -DQT_CORE_LIB -o /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/tvconfig.moc /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tvconfig.h

tv-manager.moc: ../tv-manager.h
	$(CMAKE_COMMAND) -E cmake_progress_report /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/CMakeFiles $(CMAKE_PROGRESS_6)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating tv-manager.moc"
	/usr/qt/4/bin/moc -I/usr/qt/4/include -I/usr/qt/4/include/QtGui -I/usr/qt/4/include/QtXml -I/usr/qt/4/include/QtCore -I/usr/qt/4/include/QtXmlPatterns -I/usr/qt/4/include/QtWebKit -I/usr/qt/4/include/QtHelp -I/usr/qt/4/include/QtAssistant -I/usr/qt/4/include/QtDBus -I/usr/qt/4/include/QtTest -I/usr/qt/4/include/QtUiTools -I/usr/qt/4/include/QtScript -I/usr/qt/4/include/QtSvg -I/usr/qt/4/include/QtSql -I/usr/qt/4/include/QtOpenGL -I/usr/qt/4/include/QtNetwork -I/usr/qt/4/include/QtDesigner -I/usr/qt/4/include/Qt3Support -I/usr/qt/4/mkspecs/default -I/home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/-DQT_DLL -I/usr/kde/4/include -I/usr/kde/4/include/KDE -I/usr/qt/4/include/KDE -I/home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build -I/usr/include/pci -D_BSD_SOURCE -DQT_DLL -DQT_GUI_LIB -DQT_XML_LIB -DQT_CORE_LIB -o /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/tv-manager.moc /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/tv-manager.h

# Object files for target tv-manager
tv__manager_OBJECTS = \
"CMakeFiles/tv-manager.dir/main.o" \
"CMakeFiles/tv-manager.dir/tvconfig.o" \
"CMakeFiles/tv-manager.dir/tvconfigui.o" \
"CMakeFiles/tv-manager.dir/tv-manager.o"

# External object files for target tv-manager
tv__manager_EXTERNAL_OBJECTS =

tv-manager: CMakeFiles/tv-manager.dir/main.o
tv-manager: CMakeFiles/tv-manager.dir/tvconfig.o
tv-manager: CMakeFiles/tv-manager.dir/tvconfigui.o
tv-manager: CMakeFiles/tv-manager.dir/tv-manager.o
tv-manager: /usr/qt/4/lib/libQtGui.so
tv-manager: /usr/lib/libpng.so
tv-manager: /usr/lib/libSM.so
tv-manager: /usr/lib/libICE.so
tv-manager: /usr/lib/libXrender.so
tv-manager: /usr/lib/libfreetype.so
tv-manager: /usr/lib/libfontconfig.so
tv-manager: /usr/lib/libXext.so
tv-manager: /usr/lib/libX11.so
tv-manager: /usr/lib/libm.so
tv-manager: /usr/qt/4/lib/libQtXml.so
tv-manager: /usr/qt/4/lib/libQtCore.so
tv-manager: /lib/libz.so
tv-manager: /usr/lib/libgthread-2.0.so
tv-manager: /usr/lib/libglib-2.0.so
tv-manager: /usr/lib/librt.so
tv-manager: /usr/kde/4/lib/libkdeui.so.5.2.0
tv-manager: /usr/kde/4/lib/libkdecore.so.5.2.0
tv-manager: /usr/qt/4/lib/libQtDBus.so
tv-manager: /usr/qt/4/lib/libQtCore.so
tv-manager: /usr/qt/4/lib/libQtSvg.so
tv-manager: /usr/qt/4/lib/libQtGui.so
tv-manager: CMakeFiles/tv-manager.dir/build.make
tv-manager: CMakeFiles/tv-manager.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable tv-manager"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tv-manager.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/tv-manager.dir/build: tv-manager
.PHONY : CMakeFiles/tv-manager.dir/build

CMakeFiles/tv-manager.dir/requires: CMakeFiles/tv-manager.dir/main.o.requires
CMakeFiles/tv-manager.dir/requires: CMakeFiles/tv-manager.dir/tvconfig.o.requires
CMakeFiles/tv-manager.dir/requires: CMakeFiles/tv-manager.dir/tvconfigui.o.requires
CMakeFiles/tv-manager.dir/requires: CMakeFiles/tv-manager.dir/tv-manager.o.requires
.PHONY : CMakeFiles/tv-manager.dir/requires

CMakeFiles/tv-manager.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/tv-manager.dir/cmake_clean.cmake
.PHONY : CMakeFiles/tv-manager.dir/clean

CMakeFiles/tv-manager.dir/depend: tvconfig.moc
CMakeFiles/tv-manager.dir/depend: tv-manager.moc
	cd /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build /home/albayenes/svn/uludag/trunk/staj-projeleri/tv-manager/src/build/CMakeFiles/tv-manager.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/tv-manager.dir/depend

