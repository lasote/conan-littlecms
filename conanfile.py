from conans import ConanFile, ConfigureEnvironment
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake


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

    def source(self):
        zip_name = "lcms2-%s.tar.gz" % self.version
        download("http://downloads.sourceforge.net/project/lcms/lcms/2.7/%s" % zip_name, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

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
            print(env.command_line)
            self.run("cd %s && %s ./configure" % (self.ZIP_FOLDER_NAME, env.command_line))
            self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, env.command_line))
        else:
            pass

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src="", keep_path=False)
                self.copy(pattern="*.lib", dst="lib", src="", keep_path=False)
            else:
                self.copy(pattern="*.lib", dst="lib", src="", keep_path=False)
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
            pass
        else:
            self.cpp_info.libs = ['lcms2', 'm']
