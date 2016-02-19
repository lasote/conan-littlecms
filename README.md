[![Build Status](https://travis-ci.org/lasote/conan-littlecms.svg)](https://travis-ci.org/lasote/conan-littlecms)


# conan-littlecms

[Conan.io](https://conan.io) package for LittleCMS library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/littlecms/2.7/lasote/stable).

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload littlecms/2.7@lasote/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install littlecms/2.7@lasote/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    littlecms/2.7@lasote/stable

    [options]
    littlecms:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
