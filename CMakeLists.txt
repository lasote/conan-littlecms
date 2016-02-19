cmake_minimum_required(VERSION 3.0)

project(
    liblcms2 
    VERSION 2.6
    LANGUAGES C
)

include(FeatureSummary)

set(LCMS_VERSION_MAJOR 2)
set(LCMS_VERSION_MINOR 7)
set(LCMS_VERSION_STR "${LCMS_VERSION_MAJOR}.${LCMS_VERSION_MINOR}")

option (BUILD_SHARED_LIBS "Build Shared Libraries" ON) 
option (BUILD_TOOLS "Build Tools (most depend on JPEG & TIFF)" ON) 
option (BUILD_TESTS "Build Tests" ON) 

set(LIBTARGET "lcms2")

include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")

file(GLOB SRCS src/*.c)
file(GLOB HDRS include/*.h)

if (WIN32)
    set(runtime_name ${LIBTARGET}${MSVC_SHARED_SUFFIX_BASE})
    
    set(VER_PRODUCTNAME_STR "LittleCMS color engine")
    set(VER_ORIGINALFILENAME_STR "${runtime_name}.dll")
    set(VER_INTERNALNAME_STR ${LIBTARGET})
    set(VER_FILEDESCRIPTION_STR "LittleCMS Dynamic Link Library")
    set(VER_LEGALCOPYRIGHT_STR "Copyright (c) Marti Maria 2011.")
    set(VER_STR ${LCMS_VERSION_STR})
    set(VER_NUM "${LCMS_VERSION_MAJOR},${LCMS_VERSION_MINOR},0,0")
    configure_file(
          ${CMAKE_CURRENT_SOURCE_DIR}/src/lcms2.rc.in
          ${CMAKE_CURRENT_BINARY_DIR}/lcms2.rc
          @ONLY
      )
    set(VCSHAREDFILES src/lcms2.def ${CMAKE_CURRENT_BINARY_DIR}/lcms2.rc)
else(WIN32)
    set(runtime_name ${LIBTARGET})
endif()

if (BUILD_SHARED_LIBS)
    add_library(${LIBTARGET} SHARED ${SRCS} ${HDRS} ${VCSHAREDFILES})    
endif()
 
set_target_properties(
    ${LIBTARGET}
        PROPERTIES 
          SOVERSION ${LCMS_VERSION_MAJOR}.${LCMS_VERSION_MINOR}
          VERSION ${LCMS_VERSION_MAJOR}
          PUBLIC_HEADER "${HDRS}"
  )
