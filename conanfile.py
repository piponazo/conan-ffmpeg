from conans import ConanFile, ConfigureEnvironment, tools
import os

class GmpConan(ConanFile):
    name = "Ffmpeg"
    version = "2.8.3"
    settings = "os", "compiler", "build_type", "arch"
    FOLDER_NAME = "ffmpeg-2.8.3"

    def source(self):
        zip_name = "%s.tar.bz2" % self.FOLDER_NAME
        url = "http://ffmpeg.org/releases/ffmpeg-%s.tar.bz2" % (self.version)
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.remove(zip_name)

    def build(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        installFolder = "%s/installFolder" % os.getcwd()

        n_cores = tools.cpu_count()
        self.run("mkdir %s" % installFolder)
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
                 --prefix=%s" % (self.FOLDER_NAME, installFolder))

        self.run("cd %s && %s make -j%s" % (self.FOLDER_NAME, env.command_line, n_cores))
        self.run("cd %s && make install" % self.FOLDER_NAME)

    def package(self):
        self.copy("*.h",  dst="include", src="installFolder/include")
        self.copy("*.so", dst="lib",     src="installFolder/lib")

    def package_info(self):
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libs = ['avcodec', 'avformat', 'avfilter', 'avutil', 'swscale']
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
        self.cpp_info.resdirs = ['res']  # Directories where resources, data, etc can be found
