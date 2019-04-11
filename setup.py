#!/usr/bin/env python
from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from shio.version import version_string
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import sys
import os
import shutil

package = 'shio'

class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def run(self):
        # do not compile __init__.py file
        self.extensions = [ext for ext in self.extensions if Path(ext.name).suffix != '.__init__']
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir
        for r, d, f in os.walk(package):
            for file in f:
                if file == '__init__.py':
                    self.copy_file(Path(r) / file, root_dir, target_dir)

    def build_extensions(self):
        if hasattr(self.compiler, "compiler_so"):
            if '-Wstrict-prototypes' in self.compiler.compiler_so:
                self.compiler.compiler_so.remove('-Wstrict-prototypes')
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
        elif ct == 'msvc':
            opts.append(
                '/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
            opts.append('/DWIN32')
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)

    def copy_file(self, path, s_dir, d_dir):
        if not (s_dir / path).exists():
            return
        shutil.copyfile(str(s_dir / path), str(d_dir / path))


setup(
    name="shio",
    version=version_string,
    packages=[],
    license="MIT",
    description="A powerful declarative symmetric parser/builder for binary data support cp950",
    long_description=open("README.rst").read(),
    platforms=["POSIX", "Windows"],
    url="http://construct.readthedocs.org",
    author="Arkadiusz Bulski, Tomer Filiba, Corbin Simpson, TKHuang",
    author_email="arek.bulski@gmail.com, tomerfiliba@gmail.com, MostAwesomeDude@gmail.com, tkhuangs@gmail.com",
    ext_modules=cythonize(
        [
            Extension(
                "shio.lib.*",
                ["shio/lib/*.py"],
            ),
            Extension(
                "shio.*",
                ["shio/*.py"],
            ),
        ],
        build_dir="build",
        compiler_directives=dict(always_allow_keywords=True),
    ),
    cmdclass=dict(build_ext=BuildExt),
    install_requires=[],
    extras_require={
        "extras": [
            "enum34",
            "numpy",
            "arrow",
            "ruamel.yaml",
        ],
    },
    requires=[],
    provides=["construct"],
    keywords=[
        "construct",
        "kaitai",
        "declarative",
        "data structure",
        "struct",
        "binary",
        "symmetric",
        "parser",
        "builder",
        "parsing",
        "building",
        "pack",
        "unpack",
        "packer",
        "unpacker",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
