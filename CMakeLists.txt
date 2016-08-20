cmake_minimum_required(VERSION 3.0)
PROJECT(conanlittlecms)
include(../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

cmake_minimum_required(VERSION 3.0)

project(
    liblcms2 
    VERSION 2.7
    LANGUAGES C
)
option (BUILD_SHARED_LIBS "Build Shared Libraries" OFF) 

include(FeatureSummary)

set(LCMS_VERSION_MAJOR 2)
set(LCMS_VERSION_MINOR 7)
set(LCMS_VERSION_STR "${LCMS_VERSION_MAJOR}.${LCMS_VERSION_MINOR}")
option (BUILD_TOOLS "Build Tools (most depend on JPEG & TIFF)" ON) 

set(LIBTARGET "lcms2")

include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")

file(GLOB SRCS src/*.c)
file(GLOB HDRS include/*.h)

if(WIN32)
    set(VCSHAREDFILES src/lcms2.def Projects/VC2013/lcms2.rc)
endif()

if(BUILD_SHARED_LIBS)
    add_library(${LIBTARGET} SHARED ${SRCS} ${HDRS} ${VCSHAREDFILES})    
else()
    add_library(${LIBTARGET} STATIC ${SRCS} ${HDRS})
endif()

if (BUILD_TOOLS)
    find_package(JPEG)
    find_package(TIFF)

    set (tools_common 
        utils/common/utils.h
        utils/common/vprf.c
        utils/common/xgetopt.c
    )
    
    # linkicc
    add_executable(linkicc
        ${tools_common}
        utils/linkicc/linkicc.c
    )
    target_link_libraries(linkicc PRIVATE ${LIBTARGET})
    target_include_directories(linkicc PRIVATE utils/common)
   
    add_executable(psicc
        ${tools_common}
        utils/psicc/psicc.c
    )
    target_link_libraries(psicc PRIVATE ${LIBTARGET})
    target_include_directories(psicc PRIVATE utils/common)

    add_executable(transicc
        ${tools_common}
        utils/transicc/transicc.c
    )
    target_link_libraries(transicc PRIVATE ${LIBTARGET})
    target_include_directories(transicc PRIVATE utils/common)
    

    set (tool_targets psicc linkicc transicc)

    if (JPEG_FOUND)
        add_executable(jpgicc 
            ${tools_common}
            utils/jpgicc/iccjpeg.c
            utils/jpgicc/iccjpeg.h
            utils/jpgicc/jpgicc.c
        )
        target_link_libraries(jpgicc PRIVATE ${LIBTARGET} ${JPEG_LIBRARIES})
        target_include_directories(jpgicc PRIVATE ${JPEG_INCLUDE_DIR} utils/common)

        set (tool_targets ${tool_targets} jpgicc)

    endif(JPEG_FOUND)

    if (TIFF_FOUND)
        add_executable(tificc
            ${tools_common}
            utils/tificc/tificc.c
            )
        target_link_libraries(tificc PRIVATE  ${LIBTARGET} ${TIFF_LIBRARIES})
        target_include_directories(tificc PRIVATE ${TIFF_INCLUDE_DIR} utils/common)

        set (tool_targets ${tool_targets} tificc)
    endif()

endif()
