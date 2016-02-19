from conans import ConanFile, ConfigureEnvironment
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake
from shutil import copyfile


class ZlibNgConan(ConanFile):
    name = "littlecms"
    version = "2.7"
    ZIP_FOLDER_NAME = "lcms2-%s" % version 
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt"]
    url="http://github.com/lasote/conan-littlecms"
    license="https://github.com/mm2/Little-CMS/blob/master/COPYING"
    
    def config(self):
        
        if self.settings.os == "Windows":
            self.options.remove("shared")
        else:
            self.options.add("shared")

    def source(self):
        zip_name = "lcms2-%s.tar.gz" % self.version
        download("http://downloads.sourceforge.net/project/lcms/lcms/2.7/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)
        else:
            copyfile("CMakeLists.txt", os.path.join(self.ZIP_FOLDER_NAME, "CMakeLists.txt"))

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            
            if self.settings.os == "Macos":
                old_str = 'install_name \$rpath/\$soname'
                new_str = 'install_name \$soname'
                replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
            
            env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
            self.run("cd %s && %s ./configure" % (self.ZIP_FOLDER_NAME, env.command_line))
            self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, env.command_line))
        else:
            cmake = CMake(self.settings)
            self.run("cd %s && mkdir _build" % self.ZIP_FOLDER_NAME)
            cd_build = "cd %s/_build" % self.ZIP_FOLDER_NAME
            self.output.warn('%s && cmake .. %s' % (cd_build, cmake.command_line))
            self.run('%s && cmake .. %s' % (cd_build, cmake.command_line))
            self.output.warn("%s && cmake --build . %s" % (cd_build, cmake.build_config))
            self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        if self.settings.os == "Windows":
            self.copy(pattern="*lcms2.lib", dst="lib", src="", keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['lcms2']
        else:
            self.cpp_info.libs = ['lcms2', 'm']
