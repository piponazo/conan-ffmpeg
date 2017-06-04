from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class FFmpegConan(ConanFile):
    name = "FFmpeg"
    version = "3.3"
    description = "Conan recipe for FFMpeg"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/piponazo/conan-ffmpeg"
    license = "LGPL v2.1+"
    #exports = ["patches/*.patch"]
    exports = ['FindFFmpeg.cmake']

    def source(self):
        self.run("git clone --depth 1 --branch n%s https://github.com/FFmpeg/FFmpeg" % self.version)

    def build(self):
        env = AutoToolsBuildEnvironment(self)

        n_cores = tools.cpu_count()
        CC = os.getenv('CC')
        CXX = os.getenv('CXX')

        with tools.environment_append(env.vars):
            self.run("cd %s && ./configure \
                     --enable-pic \
                     --enable-shared \
                     --disable-static \
                     --disable-symver \
                     --disable-ffplay \
                     --disable-ffprobe \
                     --enable-pthreads \
                     --disable-devices \
                     --disable-avdevice \
                     --disable-nonfree \
                     --disable-gpl \
                     --disable-doc \
                     --enable-avresample \
                     --enable-demuxer=rtsp \
                     --enable-muxer=rtsp \
                     --disable-bzlib \
                     --disable-programs \
                     --disable-swresample \
                     --cc=%s \
                     --cxx=%s \
                     --prefix=%s" % (self.name, CC, CXX, self.package_folder))

            self.run("cd %s && make -j%s" % (self.name, n_cores))
            self.run("cd %s && make install" % self.name)

    def package(self):
        self.copy('FindFFmpeg.cmake', '.', '.')
        self.copy("*.h",  dst="include", src="installFolder/include")
        self.copy("*.so", dst="lib",     src="installFolder/lib")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]  # Ordered list of include paths
        self.cpp_info.libs = ["avcodec", "avformat", "avfilter", "avutil", "swscale"]
        self.cpp_info.libdirs = ["lib"]  # Directories where libraries can be found
