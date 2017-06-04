from conans import ConanFile, CMake
import os

# This easily allows to copy the package in other user or channel
username = os.getenv("CONAN_USERNAME", "piponazo")
channel = os.getenv("CONAN_CHANNEL", "test")

class GmpReuseConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "FFmpeg/3.3@%s/%s" % (username, channel)
    generators = "cmake"

    def imports(self):
        self.copy('*.so*', src='lib', dst='bin')

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        # equal to ./bin/greet, but portable win: .\bin\greet
        self.run(os.sep.join([".","bin", "testApp"]))
