cmake_minimum_required(VERSION 2.6)
project(jsoncpp)
enable_testing()

option(JSONCPP_WITH_TESTS "Compile and run JsonCpp test executables" ON)
option(JSONCPP_WITH_POST_BUILD_UNITTEST "Automatically run unit-tests as a post build step" ON)
option(JSONCPP_WITH_WARNING_AS_ERROR "Force compilation to fail if a warning occurs" OFF)

# Ensures that CMAKE_BUILD_TYPE is visible in cmake-gui on Unix
if(NOT WIN32)
    if(NOT CMAKE_BUILD_TYPE)
        set(CMAKE_BUILD_TYPE Release CACHE STRING
            "Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel Coverage."
            FORCE)
    endif(NOT CMAKE_BUILD_TYPE)
endif(NOT WIN32)

# This ensures shared DLL are in the same dir as executable on Windows.
# Put all executables / libraries are in a project global directory.
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib
    CACHE PATH "Single directory for all static libraries.")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib
    CACHE PATH "Single directory for all dynamic libraries on Unix.")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin
    CACHE PATH "Single directory for all executable and dynamic libraries on Windows.")
mark_as_advanced( CMAKE_RUNTIME_OUTPUT_DIRECTORY CMAKE_LIBRARY_OUTPUT_DIRECTORY CMAKE_ARCHIVE_OUTPUT_DIRECTORY )

# Extract major, minor, patch and qualifier from version text
# Parse a version string "X.Y.Z[-qualifier]" and outputs
# version parts in ${OUPUT_PREFIX}_MAJOR, _MINOR, _PATCH, _QUALIFIER.
# If parse succed then ${OUPUT_PREFIX}_FOUND is TRUE.
macro(jsoncpp_parse_version VERSION_TEXT OUPUT_PREFIX)
    set(VERSION_REGEX "[0-9]+\\.[0-9]+\\.[0-9]+(-[a-zA-Z0-9_]+)?")
    if( ${VERSION_TEXT} MATCHES ${VERSION_REGEX} )
        string(REGEX MATCHALL "[0-9]+|-([A-Za-z0-9_]+)" VERSION_PARTS ${VERSION_TEXT})
        list(APPEND VERSION_PARTS "") # empty qualifier to handle no qualifier case
        list(GET VERSION_PARTS 0 ${OUPUT_PREFIX}_MAJOR)
        list(GET VERSION_PARTS 1 ${OUPUT_PREFIX}_MINOR)
        list(GET VERSION_PARTS 2 ${OUPUT_PREFIX}_PATCH)
        list(GET VERSION_PARTS 3 ${OUPUT_PREFIX}_QUALIFIER)
        set( ${OUPUT_PREFIX}_FOUND TRUE )
    else( ${VERSION_TEXT} MATCHES ${VERSION_REGEX} )
        set( ${OUPUT_PREFIX}_FOUND FALSE )
    endif( ${VERSION_TEXT} MATCHES ${VERSION_REGEX} )
endmacro(jsoncpp_parse_version)

# Read out version from "version" file
file(STRINGS "version" JSONCPP_VERSION)

jsoncpp_parse_version( ${JSONCPP_VERSION} JSONCPP_VERSION )
if(NOT JSONCPP_VERSION_FOUND)
    message(FATAL_ERROR "Failed to parse version string properly. Expect X.Y.Z[-qualifier]")
endif(NOT JSONCPP_VERSION_FOUND)

message(STATUS "JsonCpp Version: ${JSONCPP_VERSION_MAJOR}.${JSONCPP_VERSION_MINOR}.${JSONCPP_VERSION_PATCH}${JSONCPP_VERSION_QUALIFIER}")
# File version.h is only regenerated on CMake configure step
configure_file( "${PROJECT_SOURCE_DIR}/src/lib_json/version.h.in"
                "${PROJECT_SOURCE_DIR}/include/json/version.h" )

macro(UseCompilationWarningAsError)
    if ( MSVC )
        # Only enabled in debug because some old versions of VS STL generate
        # warnings when compiled in release configuration.
        set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /WX ")
    endif( MSVC )
endmacro()

# Include our configuration header
include_directories( ${CMAKE_SOURCE_DIR}/include )

if ( MSVC )
    # Only enabled in debug because some old versions of VS STL generate
    # unreachable code warning when compiled in release configuration.
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /W4 ")
endif( MSVC )

if(JSONCPP_WITH_WARNING_AS_ERROR)
    UseCompilationWarningAsError()
endif(JSONCPP_WITH_WARNING_AS_ERROR)

# Build the different applications
add_subdirectory( src )

#install the includes
add_subdirectory( include )
