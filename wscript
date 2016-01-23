#! /usr/bin/env python
# encoding: utf-8
# Thomas Nagy, 2006-2010 (ita)

# the following two variables are used by the target "waf dist"
VERSION = '0.0.1'
APPNAME = 'fastkmeans'

INCLUDES = [
    'include',
]
SOURCES = [
    'src/fastkmeans/main.c',
    'src/fastkmeans/fastkmeans.c',
]

SHLIBS = [
    'pthread',
    'gsl',
    'm',
    'openblas',
]
STLIBS = []
USES = [
]

# Constants
str_release = 'release'
str_debug = 'debug'
BUILD_VERSIONS = [str_release, str_debug]

CFLAGS = {
    str_release: [
        '-O2',
    ],
    str_debug: [
        '-g',
    ],
    'general': [
        '--std=c11',
        '--pedantic',
        '-Werror',
        '-Wall',
        '-Wextra',
        '-Wfatal-errors',
        '-Wno-unused',
    ]
}
DEFINES = {
    str_release: [
        'ISDEBUG=0',
    ],
    str_debug: [
        'ISDEBUG=1',
    ],
    'general': [
    ]
}

# these variables are mandatory ('/' are converted automatically)
top = '.'
out = 'build'

def options(opt):
    opt.load('compiler_c')

def configure(conf):
    conf.load('compiler_c')
    conf.check(header_name='stdio.h', features='c cprogram', mandatory=True)
    conf.check(header_name='pthread.h', features='c cprogram', mandatory=True)

def build(bld):
    if not bld.variant in BUILD_VERSIONS:
        bld.fatal('Call \n    "./waf build_debug" or \n' +
                  './waf clean_debug"\nor the equivalent for release')

    cflags = CFLAGS['general'] + CFLAGS[bld.variant]
    defines = DEFINES['general'] + DEFINES[bld.variant]

    bld.program(
        source=SOURCES,
        includes=INCLUDES,
        target=APPNAME,
        use=USES,
        lib=SHLIBS,
        defines=defines,
        # libpath=,
        stlib=STLIBS,
        # stlibpath=,
        cflags=cflags,
    )



from waflib.Build import BuildContext, CleanContext
from waflib.Build import InstallContext, UninstallContext

for x in BUILD_VERSIONS:
    for y in (BuildContext, CleanContext, InstallContext, UninstallContext):
        name = y.__name__.replace('Context', '').lower()
        class tmp(y):
            cmd = name + '_' + x
            variant = x
