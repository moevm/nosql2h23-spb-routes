# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
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
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/drdrew/Projects/semester7/nrd/hello_world/build

# Include any dependencies generated for this target.
include CMakeFiles/Summator.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/Summator.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/Summator.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/Summator.dir/flags.make

CMakeFiles/Summator.dir/difficult_func.cpp.o: CMakeFiles/Summator.dir/flags.make
CMakeFiles/Summator.dir/difficult_func.cpp.o: /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/difficult_func.cpp
CMakeFiles/Summator.dir/difficult_func.cpp.o: CMakeFiles/Summator.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/drdrew/Projects/semester7/nrd/hello_world/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/Summator.dir/difficult_func.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/Summator.dir/difficult_func.cpp.o -MF CMakeFiles/Summator.dir/difficult_func.cpp.o.d -o CMakeFiles/Summator.dir/difficult_func.cpp.o -c /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/difficult_func.cpp

CMakeFiles/Summator.dir/difficult_func.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Summator.dir/difficult_func.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/difficult_func.cpp > CMakeFiles/Summator.dir/difficult_func.cpp.i

CMakeFiles/Summator.dir/difficult_func.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Summator.dir/difficult_func.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/difficult_func.cpp -o CMakeFiles/Summator.dir/difficult_func.cpp.s

CMakeFiles/Summator.dir/wrapper_func.cpp.o: CMakeFiles/Summator.dir/flags.make
CMakeFiles/Summator.dir/wrapper_func.cpp.o: /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/wrapper_func.cpp
CMakeFiles/Summator.dir/wrapper_func.cpp.o: CMakeFiles/Summator.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/drdrew/Projects/semester7/nrd/hello_world/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/Summator.dir/wrapper_func.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/Summator.dir/wrapper_func.cpp.o -MF CMakeFiles/Summator.dir/wrapper_func.cpp.o.d -o CMakeFiles/Summator.dir/wrapper_func.cpp.o -c /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/wrapper_func.cpp

CMakeFiles/Summator.dir/wrapper_func.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/Summator.dir/wrapper_func.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/wrapper_func.cpp > CMakeFiles/Summator.dir/wrapper_func.cpp.i

CMakeFiles/Summator.dir/wrapper_func.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/Summator.dir/wrapper_func.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module/wrapper_func.cpp -o CMakeFiles/Summator.dir/wrapper_func.cpp.s

# Object files for target Summator
Summator_OBJECTS = \
"CMakeFiles/Summator.dir/difficult_func.cpp.o" \
"CMakeFiles/Summator.dir/wrapper_func.cpp.o"

# External object files for target Summator
Summator_EXTERNAL_OBJECTS =

libSummator.so: CMakeFiles/Summator.dir/difficult_func.cpp.o
libSummator.so: CMakeFiles/Summator.dir/wrapper_func.cpp.o
libSummator.so: CMakeFiles/Summator.dir/build.make
libSummator.so: CMakeFiles/Summator.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/drdrew/Projects/semester7/nrd/hello_world/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX shared library libSummator.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Summator.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/Summator.dir/build: libSummator.so
.PHONY : CMakeFiles/Summator.dir/build

CMakeFiles/Summator.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/Summator.dir/cmake_clean.cmake
.PHONY : CMakeFiles/Summator.dir/clean

CMakeFiles/Summator.dir/depend:
	cd /home/drdrew/Projects/semester7/nrd/hello_world/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module /home/drdrew/Projects/semester7/nrd/hello_world/cpp_module /home/drdrew/Projects/semester7/nrd/hello_world/build /home/drdrew/Projects/semester7/nrd/hello_world/build /home/drdrew/Projects/semester7/nrd/hello_world/build/CMakeFiles/Summator.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/Summator.dir/depend

