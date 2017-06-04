find_path(FFMPEG_INCLUDE_DIR NAMES libavcodec/avcodec.h PATHS ${CONAN_INCLUDE_DIRS_FFMPEG})

foreach(FFMPEG_MODULE ${CONAN_LIBS_FFMPEG})
    find_library(LIB_${FFMPEG_MODULE} NAMES ${FFMPEG_MODULE} PATHS ${CONAN_LIB_DIRS_FFMPEG})
    list(APPEND FFMPEG_LIBRARIES ${LIB_${FFMPEG_MODULE}})
endforeach()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(FFmpeg DEFAULT_MSG FFMPEG_LIBRARIES FFMPEG_INCLUDE_DIR)
