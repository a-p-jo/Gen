#! /usr/bin/env python3

#DEFAULTS :
IF_DARWIN_AND_CLANG_MAKE_UNIVERSALS = True
PRINT_PROGRESS = True

OPTIMIZATION_CMD = ""
WARNING_CMD = ""
INVOKE_CC = "cc"

'''
# Import :
# sys for CL args
# os for sending shell cmds
# platform for system info
'''
import sys
import os
import platform

argc = len(sys.argv)
argv = sys.argv

'''
# ./make [source file(s)] [output file]  [warning level (OPTIONAL)] [optimization level (OPTIONAL)]
'''

'''System Information Analysis
# Get operating system name
# Check if POSIX system
# Get compiler name
# Check if compiler is Clang/GCC
'''
Operating_System = platform.system()
Supported_OS = os.name == "posix"

compiler = platform.python_compiler()
Supported_Compiler = "GCC" in compiler or "Clang" in compiler 

'''
# Check if number of arguments, the platform and the compiler are supported
'''

if argc >= 3 and Supported_OS and Supported_Compiler :
    sources = argv[1]
    outfile = argv[2]
    space = " "
    quote = '"'

    if argc >= 5:
        '''
        # If there are more arguments , consider them; if valid ints,
        # create suitable warning and optimization compilation options.   
        '''
        warning_number = int(argv[3])
        optimization_number = int(argv[4])

        if warning_number == 0 :
            WARNING_CMD = "-w"

        elif warning_number == 1:
            WARNING_CMD = "-Wall"

        elif warning_number == 2:
            WARNING_CMD = "-Wall -Wextra -pedantic"

        elif warning_number == 3:
            if "Clang" in compiler :
                WARNING_CMD = "-Weverything"
            else :
                WARNING_CMD = "-Wall -Wextra -pedantic -Wconversion"

        else :
            print("Invalid warning option. Used defaults...")

        '''
        # Similarly for optimization.
        #
        # Note that we are not concerned with optimizing for size or compile-time.
        # This can certainly be added as a feature later but wasn't necessary to me
        # so was not bothered with.
        '''

        if optimization_number == 1 :
            OPTIMIZATION_CMD = "-o1"

        elif optimization_number == 2 :
            OPTIMIZATION_CMD = "-o2"

        elif optimization_number == 3 :
            OPTIMIZATION_CMD = "-o3"

        else :
            print("Invalid optimization input. Used defaults...")

    '''
    # Now check the OS, compiler and relevant setting to see if compilation will be "normal" or a
    # "Universal App" is to be made.
    #
    # If macOS with Clang is detected, and it is allowed, make the x86_64 binary and the arm64 binary.
    # then use lipo to combine them into a "universal app" as demonstrated at source. Then, delete those binaries.
    #
    # Source : https://developer.apple.com/documentation/xcode/building_a_universal_macos_binary 
    #
    # Otherwise, just combine all compilation options into a string and execute the compilation
    # command.
    #
    # In either conditions, print progress step-by-step if allowed.
    '''
    
    if Operating_System == "Darwin" and "Clang" in compiler and IF_DARWIN_AND_CLANG_MAKE_UNIVERSALS :
        x86_outfile = ".temp_x86_" + outfile
        COMPILE_x86_64 = INVOKE_CC + space + WARNING_CMD + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + x86_outfile + quote

        if PRINT_PROGRESS :
            print("(x86_64)",COMPILE_x86_64)

        os.system(COMPILE_x86_64)

        arm_outfile = ".temp_arm_" + outfile
        COMPILE_ARM_64 = INVOKE_CC + space + "-w" + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + arm_outfile + quote + space + "-target arm64-apple-macos11"

        if PRINT_PROGRESS :
            print("(arm64)",COMPILE_ARM_64)

        os.system(COMPILE_ARM_64)

        LIPO_COMBINE = "lipo -create -output" + space + quote  + outfile + quote + space + quote + x86_outfile + quote + space + quote + arm_outfile + quote

        if PRINT_PROGRESS :
            print("(lipo)",LIPO_COMBINE)

        os.system(LIPO_COMBINE)

        CLEANUP = "rm" + space + quote + x86_outfile + quote + space + quote + arm_outfile + quote

        if PRINT_PROGRESS :
            print("(cleanup)",CLEANUP)

        os.system(CLEANUP)

    else :
        COMPILE = INVOKE_CC + space + WARNING_CMD + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + outfile + quote

        if PRINT_PROGRESS :
            print(COMPILE)

        os.system(COMPILE)

else:

    '''
    # Output the failure to run and its cause
    '''

    print("Failed : ",end="")

    if argc < 3:
        print("Not enough arguments.")

    elif  not Supported_OS :
        print("Unsupported non-POSIX OS.")

    elif not Supported_Compiler :
        print("Unsupported compiler.")
