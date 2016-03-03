from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="littlecms:shared", pure_c=True)
    if platform.system() == "Windows":
        # Remove shared builds in windows
        static_builds = []
        for build in builder.builds:
            if not build[1]["littlecms:shared"]:
                static_builds.append([build[0], {}])
            
        builder.builds = static_builds   

    builder.run()
