PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(test test.c)
TARGET_LINK_LIBRARIES(test ${CONAN_LIBS})

