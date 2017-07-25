from conans import ConanFile, AutoToolsBuildEnvironment, tools

class FFmpegConan(ConanFile):
    name = "FFmpeg"
    version = "3.3"
    description = "Conan recipe for FFMpeg"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/piponazo/conan-ffmpeg"
    license = "LGPL v2.1+"
    exports = ['FindFFmpeg.cmake']

    def source(self):
        self.run("git clone --depth 1 --branch n%s https://github.com/FFmpeg/FFmpeg" % self.version)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_args = ['--enable-pic',
                    '--enable-shared',
                    '--disable-static',
                    '--disable-symver',
                    '--disable-ffplay',
                    '--disable-ffprobe',
                    '--disable-devices',
                    '--disable-avdevice',
                    '--disable-nonfree',
                    '--disable-gpl',
                    '--disable-doc',
                    '--enable-avresample',
                    '--enable-demuxer=rtsp',
                    '--enable-muxer=rtsp',
                    '--disable-bzlib',
                    '--disable-programs',
                    '--disable-swresample',
                    '--prefix=%s' % self.package_folder,
                   ]

        #if self.settings.os == "Windows":
        #        #CC = os.getenv('CC')
        #        #CXX = os.getenv('CXX')
        #         #--cc=%s \
        #         #--cxx=%s \
        #    configure_command += " --arch=x86 --target-os=mingw32 --enable-cross-compile"

        env_build.configure(configure_dir = self.name, args=env_args)
        env_build.make(args = ['-j%s' % tools.cpu_count()] )

        if not tools.os_info.is_windows:
            env_build.make(args = ['install'] )

    def package(self):
        if tools.os_info.is_windows:
            self.copy('FindFFmpeg.cmake', '.', '.')
            self.copy(pattern="*.h", dst="include/libavcodec", src="%s/libavcodec" % self.name)
            self.copy(pattern="*.a", dst="lib/", src="%s/libavcodec" % self.name)
            self.copy(pattern="*.dll", dst="bin/", src="%s/libavcodec" % self.name)
        else:
            self.copy('FindFFmpeg.cmake', '.', '.')
            self.copy("*.h",  dst="include", src="installFolder/include")
            self.copy("*.so", dst="lib",     src="installFolder/lib")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]  # Ordered list of include paths
        self.cpp_info.libs = ["avcodec", "avformat", "avfilter", "avutil", "swscale"]
        self.cpp_info.libdirs = ["lib"]  # Directories where libraries can be found
