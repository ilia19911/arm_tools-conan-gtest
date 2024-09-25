from conan import ConanFile, tools
from conan.tools.scm import Git
from conan.tools.cmake import CMake
from conan.tools.files import get, copy
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
import os


class ArmGccConan(ConanFile):
    name = "gtest"
    license = "GPL-3.0-only"
    homepage = ""
    author = "Ostanin <iahve1991@gmail.com>"
    description = "gtests"
    topics = ("conan", "gtest", "arm")
    settings = "os", "arch", "compiler", "build_type"
    package_type = "application"
    exports_sources = "CMakeLists.txt"
    generators = "CMakeDeps", "CMakeToolchain"
    url = "https://github.com/google/googletest.git"

    # generators = "CMakeDeps"

    def system_requirements(self):
        print("GTEST_PYTHON_REQUIREMENTS")

    def requirements(self):
        print("REQUIRES")
        # Указываем зависимости от тулчейнов
        self.requires("gcc/13")

    def validate(self):
        print("GTEST_VALIDATION")

    def package_id(self):
        print("GTEST_PACKAGE_ID")

    def source(self):
        print("GTEST_SOURCE")
        tag = self.version
        git = Git(self)
        if not os.path.exists("./gtest"):
            git.clone(self.url, "./gtest")
            print("project cloned. It contains..")
            self.run(f"ls -la ./gtest")
            self.run(f"cd ./gtest && git checkout {tag}")


    def generate(self):
        toolchain = tools.cmake.CMakeToolchain.filename
        with open(toolchain, 'r') as template_file:
            template_content = template_file.read()
        with open(toolchain, "w") as file:
            file.write(template_content)
            file.write("include(arm-gcc-toolchain)\n")


    def build(self):
        print("GTEST_BUILD")
        cmake = CMake(self)

        cmake.configure( cli_args=[f"-B {self.package_folder}/build"])
        self.run(f"cmake --build {self.package_folder}/build -j32")
        self.run(f"cmake --install {self.package_folder}/build/  --prefix {self.package_folder}")

    def package(self):
        print("GTEST_PACKAGE")

        # self.run(f"ls -la .")
        copy(self, "source_url.txt", dst=self.package_folder, src=self.source_folder)
        copy(self, "*.cmake", dst=self.package_folder + "/cmake", src=self.source_folder)
        copy(self, "gtest/*", dst=self.package_folder, src=self.source_folder)

    def package_info(self):
        print("gtest_PACKAGE_INFO")
        # for cpu in self.arm_cpus:
        gtest_path = os.path.join(self.package_folder, "lib/cmake/GTest")
        print(f"gtest lib path is {gtest_path}")
        self.cpp_info.builddirs.append(gtest_path)

    def package_id(self):
        print("GCC_PACKAGE_ID")
        # if self.settings_target is not None:
        self.info.settings_target = self.settings_target
        self.info.settings_target.rm_safe("compiler")
        self.info.settings_target.rm_safe("build_type")
        # self.info.settings_target.os = self.info.settings.os
        # self.info.settings_target.arch = self.info.settings.arch
        # self.info.settings.rm_safe("os")
        self.info.settings.rm_safe("compiler.cppstd")
        # self.info.settings.rm_safe("os")
        # self.info.settings.rm_safe("arch")
        self.info.settings.rm_safe("build_type")
        # self.info.settings.rm_safe("compiler")
        self.info.settings.rm_safe("compiler.libcxx")

#conan list gtest/*:*

#conan create . --version=v1.15.2 -pr:h=./profiles/darwin -pr:b=./profiles/darwin -r=arm-tools --build-require

#conan upload gtest/v1.15.2 -r=arm-tools

