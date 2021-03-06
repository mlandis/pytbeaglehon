#! /usr/bin/env python
# Copyright (c) 2010-2011 by Mark T. Holder
# (see bottom of file)
import ez_setup
import sys, os
from setuptools import setup, find_packages, Extension

###############################################################################
# setuptools/distutils/etc. import and configuration

try:
    import ez_setup
    try:
        ez_setup_path = " ('" + os.path.abspath(ez_setup.__file__) + "')"
    except OSError:
        ez_setup_path = ""
    sys.stderr.write("using ez_setup%s\n" %  ez_setup_path)
    ez_setup.use_setuptools()
    import setuptools
    try:
        setuptools_path = " ('" +  os.path.abspath(setuptools.__file__) + "')"
    except OSError:
        setuptools_path = ""
    sys.stderr.write("using setuptools%s\n" % setuptools_path)
    from setuptools import setup, find_packages
except ImportError, e:
    sys.stderr.write("using distutils\n")
    from distutils.core import setup
    sys.stderr.write("using canned package list\n")
    PACKAGES = ['pytbeaglehon',
                'pytbeaglehon.ccore',
               ]
    EXTRA_KWARGS = {}
else:
    sys.stderr.write("searching for packages\n")
    PACKAGES = find_packages()
    EXTRA_KWARGS = dict(
        install_requires = ['setuptools'],
        include_package_data=True,
        test_suite = "pytbeaglehon.tests"
    )

args = sys.argv
help_msg = """
pybeathon specific options:

Compilation flags
    --debug         compile in debug mode
    --no-inline     use this if your compiler does not deal with the "inline"
                    keyword.
    --use-ncl       enable functions that depend on the NEXUS Class library.

Note that the build is sensitive to your CFLAGS environmental variable (and 
    a simple "split" call is used to break the value of the variable into 
    arguments, use of quoted strings with spaces may cause problems).

Environmental variables
BEAGLE_VERSION  The full version appended to the beaglelib. Default: 1
BEAGLE_PREFIX The directory used as the prefix for the beagle install
    Default: /usr/local

BEAGLE_DEPENDENCY_LIB The name of any dynamic library that beagle needs to 
    link with (for instance "cuda"). Default: none
BEAGLE_DEPENDENCY_LIB_DIR The directory that holds libraries that beagle needs
    to link to (eg. the "/usr/local/cuda/lib" to find the CUDA libraries).
    Default: none
    
NCL_PREFIX  The directory used as the prefix for the NCL install (only used 
    --use-ncl
"""

if ("--help" in args) or ("-h" in args):
    sys.stderr.write(help_msg)
if "--debug" in args:
    kDebugPrint = "1"
    extra_compile_args = ["-Wall"]
else:
    kDebugPrint = "0"
    extra_compile_args = []
if 'CFLAGS' in os.environ:
    extra_compile_args.extend(os.environ['CFLAGS'].split())

if "--no-inline" in args:
    have_inline = 0
    args.remove("--no-inline")
else:
    have_inline = 1
if "--use-ncl" in args:
    have_ncl = 1
else:
    have_ncl = 0
if "--trace-printing" in args:
    if kDebugPrint != "1":
        sys.stderr.write("Warning: --trace-printing only has an effect if --debug is also specified\n")
    kTracePrint = "1"
    args.remove("--trace-printing")
else:
    kTracePrint = "0"








PACKAGE_DIRS = [p.replace(".", os.path.sep) for p in PACKAGES]
PACKAGE_INFO = [("% 40s : %s" % p) for p in zip(PACKAGES, PACKAGE_DIRS)]
sys.stderr.write("packages identified:\n%s\n" % ("\n".join(PACKAGE_INFO)))

SCRIPT_SUBPATHS = [
    ['scripts', 'gtr_prob_mat.py'],
]
SCRIPTS = [os.path.join(*i) for i in SCRIPT_SUBPATHS]
sys.stderr.write("\nscripts identified: %s\n" % ", ".join(SCRIPTS))



include_dirs = []
library_dirs = []
libraries = []
preprocessor_defines =[("DEBUG_PRINTING", kDebugPrint),
                       ("API_TRACE_PRINTING", kTracePrint),
                       ("BEAGLE_API_TRACE_PRINTING", kTracePrint),
                       ("BUILDING_FOR_PYTHON", 1),
                       ("HAVE_INLINE", have_inline),
                       ("HAVE_NCL", have_ncl)
                      ]
beagle_full_version = os.environ.get("BEAGLE_VERSION")
if beagle_full_version is None:
    beagle_full_version = "1"
    sys.stderr.write('BEAGLE_VERSION not found in environment...  Assuming "%s"\n' % beagle_full_version)
beagle_version = ".".join(beagle_full_version.split(".")[:2])

beagle_lib_dir = os.environ.get('BEAGLE_PREFIX')
if not beagle_lib_dir:
    beagle_lib_dir = "/usr/local"
    sys.stderr.write('BEAGLE_PREFIX not found in environment...  Assuming "%s"\n' % beagle_lib_dir)

if not os.path.exists(beagle_lib_dir):
    sys.exit("Could not find the directory %s" % beagle_lib_dir)

beagle_lib_inc_dir = os.path.join(beagle_lib_dir, "include", "libhmsbeagle-%s" % beagle_version)
if not os.path.exists(beagle_lib_inc_dir):
    sys.exit("Could not find the directory %s" % beagle_lib_inc_dir)

beagle_lib_lib_dir = os.path.join(beagle_lib_dir, "lib")
if not os.path.exists(beagle_lib_lib_dir):
    sys.exit("Could not find the directory %s" % kbeagle_lib_lib_dir)
include_dirs.append(beagle_lib_inc_dir)
library_dirs.append(beagle_lib_lib_dir)

cuda_lib_dir = os.environ.get('BEAGLE_DEPENDENCY_LIB_DIR')
if cuda_lib_dir is None:
    sys.stderr.write('BEAGLE_DEPENDENCY_LIB_DIR not found in environment...  Assuming no additional directories to be added to the link path\n')
else:
    library_dirs.append(cuda_lib_dir)
cuda_lib = os.environ.get('BEAGLE_DEPENDENCY_LIB')
if cuda_lib is None:
    sys.stderr.write('BEAGLE_DEPENDENCY_LIB not found in environment...  Assuming no additional libraries to be added to the link path\n')
else:
    libraries.append(cuda_lib)
libraries.append('hmsbeagle')

using_ncl = "--use-ncl" in args
if using_ncl:
    args.remove("--use-ncl")
    ncl_install_dir = os.environ.get('NCL_PREFIX')
    if ncl_install_dir is None:
        ncl_install_dir = "/usr/local"
        sys.stderr.write('NCL_PREFIX not found in environment...  Assuming "%s"\n'% ncl_install_dir)
    if not os.path.exists(ncl_install_dir):
        sys.exit("Could not find the directory %s" % ncl_install_dir)

    ncl_inc_dir = os.path.join(ncl_install_dir, "include")
    if not os.path.exists(ncl_inc_dir):
        sys.exit("Could not find the directory %s" % ncl_inc_dir)

    ncl_lib_dir = os.path.join(ncl_install_dir, "lib", "ncl")
    if not os.path.exists(ncl_lib_dir):
        sys.exit("Could not find the directory %s" % ncl_lib_dir)
    include_dirs.append(ncl_inc_dir)
    library_dirs.append(ncl_lib_dir)
    libraries.append('ncl')


ENTRY_POINTS = {}
try:
    from setuptools import Command
except ImportError:
    sys.stderr.write("setuptools.Command could not be imported: setuptools extensions not available\n")
else:
    sys.stderr.write("setuptools command extensions are available\n")
    command_hook = "distutils.commands"
    ENTRY_POINTS[command_hook] = []

src_prefix = "pytbeaglehon/ccore"
ext_source_files =[ "asrv.c",
                    "calc_instance.c",
                    "discrete_state_model.c",
                    "phylo_util.c",
                    "py_asrv.c",
                    "py_beagle.c", 
                    "py_calc_instance.c",
                    "py_discrete_state_model.c",
                    "py_util.c", 
                  ]
ext_sources = [os.path.join(src_prefix, i) for i in ext_source_files]
setup(name = "pytbeaglehon",
      version = "0.01",
      packages=PACKAGES,
      scripts = SCRIPTS,
      entry_points = ENTRY_POINTS,
      maintainer = "Mark Holder",
      maintainer_email = "mtholder@gmail.com",
      description = "Calculations of likelihoods for phylogenetics using C extensions and the beaglelib library",
      ext_modules = [
        Extension("pytbeaglehon.ccore.disc_state_cont_time_model",
            define_macros=preprocessor_defines,
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            libraries=libraries,
            extra_compile_args=extra_compile_args,
            sources=ext_sources)],
      license = "GNU General Public License (see LICENCE.txt and GPL.txt)",
      keywords = "phylogenetics bioinformatics likelihood",
      url = "http://people.ku.edu/~mtholder",
      classifiers = [
            "Development Status :: 2 - Pre-Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "License :: OSI Approved :: GNU Library or  General Public License (GPL)",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
            ],
      **EXTRA_KWARGS
      )

################################################################################
# cPhyProb is a package implementing some probability calculations used in
#   calculating likelihoods on phylogenies.
#
# Copyright (C) 2005-2007  Mark Holder mtholder@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU  General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
# You should have received a copy of the GNU  General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
################################################################################
