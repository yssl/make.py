#!/usr/bin/env python

###########################################
# make.py
# Replacement for Makefile.
# This script should be placed in a project root src dir where CMakeLists.txt locates.
#
# Usage:
#   in terminal:
#       ./make.py rbuild [currentFilePath]
#       ./make.py dbuild [currentFilePath]
#       ./make.py rrun [currentFilePath]
#       ./make.py drun [currentFilePath]
#       ./make.py rbuildrun [currentFilePath]
#       ./make.py dbuildrun [currentFilePath]
#       ./make.py rprintbin [currentFilePath]
#       ./make.py dprintbin [currentFilePath]
#       ./make.py rclean [currentFilePath]
#       ./make.py dclean [currentFilePath]
#   or in .vimrc:
#       makeprg=stdbuf\ -i0\ -o0\ -e0\ python\ -u\ make.py\ rbuildrun\ %
#       nmap <F9> :Make<CR>

import sys, os, fnmatch
opjoin = os.path.join

# Installation path of Microsoft Visual C++ Compiler for Python 2.7 
vcbinpath = 'C:\\Users\\yoonsang\\AppData\\Local\\Programs\\Common\\Microsoft\\\"Visual C++ for Python\"\\9.0\\VC\\bin'
vcvarsallpath = 'C:\\Users\\yoonsang\\AppData\\Local\\Programs\\Common\\Microsoft\\\"Visual C++ for Python\"\\9.0'

# get projName
thisFileDir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
projName = os.path.basename(thisFileDir)

# function
def run(cmds):
    for cmd in cmds:
        ret = os.system(cmd)
        if ret!=0:
            exit(ret)

# argument processing
if len(sys.argv)==1: 
    target = 'all'
    currentFilePath = ''
elif len(sys.argv)==2: 
    target = sys.argv[1]
    currentFilePath = ''
else:
    target = sys.argv[1]
    currentFilePath = sys.argv[2]

# target processing
if target=='all':
    target = 'rbuild'

# configuration processing
if target[0]=='r':
    config = 'release'
    buildType = 'Release'
elif target[0]=='d':
    config = 'debug'
    buildType = 'Debug'

###########################################
# USER SETTING

# default build root dir is build_projName :
# parentDirOfProj/
#   - projName/
#       - make.py
#       - CMakeLists.txt
#   - build_projName
# but you can modify this line if you want to change it.
buildRootDir = os.path.abspath(opjoin(opjoin(thisFileDir, os.pardir), 'build_%s'%projName))

buildDir = opjoin(buildRootDir, config)

binPatternPaths = [
        ['*/TestsWithGUI/*','Test/TestsWithGUI/TestsWithGUI'],
        ['*/TestsWithoutGUI/*','Test/TestsWithoutGUI/TestsWithoutGUI'],
        ['*','Test/TestsWithGUI/TestsWithGUI'],
        ]

###########################################
# script

# bin file processing
binFile = projName
for pattern, binPath in binPatternPaths:
    if fnmatch.fnmatch(currentFilePath, pattern):
        if os.name=='nt':
            binPath = binPath.replace('/','\\')
        binFile = binPath
        break

print '================================================================================'
print 'make.py %s for %s'%(target, projName)
print 
print 'script location: %s'%thisFileDir
if target[1:]=='run' or target[1:]=='buildrun':
    print 'executable file path: %s'%opjoin(buildDir, binFile)
print '================================================================================'
print

# make processing
if target[1:]=='build':
    if os.name=='nt':
        run(['mkdir "%s" & cd %s && %s && cmake -D CMAKE_BUILD_TYPE=%s -G "NMake Makefiles" %s'
                %(buildDir, buildDir, opjoin(vcvarsallpath, 'vcvarsall.bat'), buildType, thisFileDir),
            'cd %s && %s && %s'%(buildDir, opjoin(vcvarsallpath, 'vcvarsall.bat'), opjoin(vcbinpath, 'nmake'))])
    else:
        run(['mkdir -p %s ; cd %s && cmake -D CMAKE_BUILD_TYPE=%s %s'
                %(buildDir, buildDir, buildType, thisFileDir),
            'cd %s && make -j$(nproc) --no-print-directory VERBOSE=1'%(buildDir)])

elif target[1:]=='run':
    if os.name=='nt':
        run(['%s'%(opjoin(buildDir, binFile))])
    else:
        run(['%s'%(opjoin(buildDir, binFile))])

elif target[1:]=='buildrun':
    buildargs = ''
    runargs = ''
    for i in range(len(sys.argv)):
        if i==1:    # target
            buildarg = target[0]+'build'
            runarg = target[0]+'run'
        else:
            buildarg = sys.argv[i]
            runarg = sys.argv[i]
        buildargs += buildarg + ' '
        runargs += runarg + ' '
    ret = os.system('python %s'%buildargs)
    if ret!=0:
        exit(ret)
    ret = os.system('python %s'%runargs)
    if ret!=0:
        exit(ret)

elif target[1:]=='printbin':
    if os.name=='nt':
        run(['echo %s'%(opjoin(buildDir, binFile))])
    else:
        run(['echo %s'%(opjoin(buildDir, binFile))])

elif target[1:]=='clean':
    if os.name=='nt':
        run(['rmdir %s /s /q'%(buildDir)])
    else:
        run(['rm -rf %s'%(buildDir)])
