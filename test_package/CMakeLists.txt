cmake_minimum_required(VERSION 3.5)
project(FFmpegTest LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_set_find_paths()

find_package(FFmpeg REQUIRED QUIET)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

message(STATUS "FFMPEG_LIBRARIES: ${FFMPEG_LIBRARIES}")
message(STATUS "FFMPEG_INCLUDE_DIR: ${FFMPEG_INCLUDE_DIR}")
message(STATUS "LIB_avformat: ${LIB_avformat}")

add_executable(testApp main.cpp)
#target_link_libraries(testApp PRIVATE ${FFMPEG_LIBRARIES})
target_link_libraries(testApp PRIVATE ${LIB_avformat} ${LIB_avcodec} ${LIB_avutil})
target_include_directories(testApp SYSTEM PRIVATE ${FFMPEG_INCLUDE_DIR})
