#! /usr/bin/env python3

#Settings :
IF_DARWIN_AND_CLANG_MAKE_UNIVERSALS = True
IF_NOT_DARWIN_COMPILE_BOTH_STATIC_AND_DYNAMIC = False
IF_NOT_BOTH_THEN_JUST_DYNAMIC = True
PRINT_PROGRESS = False
SILENCE_ALL_BUILD_TOOLS = False

#Defaults :
OPTIMIZATION_CMD = ""
WARNING_CMD = ""
INVOKE_CC = "cc"

WARNING_LEVEL_0 = "-w"
WARNING_LEVEL_1 = "-Wall"
WARNING_LEVEL_2 = "-Wall -Wextra -pedantic"
WARNING_LEVEL_3 = "-Wall -Wextra -pedantic -Wconversion"
WARNING_LEVEL_3_CLANG = "-Weverything"

OPTIMIZATION_LEVEL_1 = "-o1"
OPTIMIZATION_LEVEL_2 = "-o2"
OPTIMIZATION_LEVEL_3 = "-o3"

STATIC_BIN_PREFIX = "static_"
DYNAMIC_BIN_PREFIX = "dynamic_"

#  Format : ./gen.py [source] [output]  [warning level (OPTIONAL)] [optimization level (OPTIONAL)]

'''
# Import :
# sys for CL args
# os for sending shell cmds
# platform for system info
'''
import sys
import os
import platform

argv = sys.argv
argc = len(argv)

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
    enforce_silence = " &> /dev/null" * SILENCE_ALL_BUILD_TOOLS

    if argc >= 4:
        '''
        # If there are more arguments , consider them; if valid ints,
        # create suitable warning and optimization compilation options.   
        '''
        warning_number = int(argv[3])

        if warning_number == 0 :
            WARNING_CMD = WARNING_LEVEL_0

        elif warning_number == 1:
            WARNING_CMD = WARNING_LEVEL_1

        elif warning_number == 2:
            WARNING_CMD = WARNING_LEVEL_2

        elif warning_number == 3:
            if "Clang" in compiler :
                WARNING_CMD = WARNING_LEVEL_3_CLANG
            else :
                WARNING_CMD = WARNING_LEVEL_3

        else :
            print("Invalid warning option. Used defaults...")

        '''
        # Similarly for optimization.
        #
        # Note that we are not concerned with optimizing for size or compile-time.
        # This can certainly be added as a feature later but wasn't necessary to me
        # so was not bothered with.
        '''

        if argc >= 5:

            optimization_number = int(argv[4])

            if optimization_number == 1 :
                OPTIMIZATION_CMD = OPTIMIZATION_LEVEL_1

            elif optimization_number == 2 :
                OPTIMIZATION_CMD = OPTIMIZATION_LEVEL_2

            elif optimization_number == 3 :
                OPTIMIZATION_CMD = OPTIMIZATION_LEVEL_3

            else :
                print("Invalid optimization input. Used defaults...")

    '''
    # Now check the OS.
    #
    # If macOS is detected :
    #   if Clang is CC + making universals is allowed :
    #       -> compile an x86 binary &  compile an arm binary
    #       -> lipo them to make universal bin (see source) and the delte them.
    #   else :
    #       -> compile normally into a standard binary.
    #
    # Source : https://developer.apple.com/documentation/xcode/building_a_universal_macos_binary 
    #
    # Else :
    #   -> If configuration is set to make static AND dynamic binaries, do that.
    #   -> Else , make a normal and standard binary
    #
    # In either conditions, print progress step-by-step if allowed.
    '''
    
    if Operating_System == "Darwin" :

        if "Clang" in compiler and IF_DARWIN_AND_CLANG_MAKE_UNIVERSALS :
            x86_outfile = ".temp_x86_" + outfile
            COMPILE_x86_64 = INVOKE_CC + space + WARNING_CMD + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + x86_outfile + quote + enforce_silence

            if PRINT_PROGRESS :
                print("(x86_64)",COMPILE_x86_64)

            os.system(COMPILE_x86_64)

            arm_outfile = ".temp_arm_" + outfile
            COMPILE_ARM_64 = INVOKE_CC + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + arm_outfile + quote + space + "-target arm64-apple-macos11" + space + "&> /dev/null"

            if PRINT_PROGRESS :
                print("(arm64)",COMPILE_ARM_64)

            os.system(COMPILE_ARM_64)

            LIPO_COMBINE = "lipo -create -output" + space + quote  + outfile + quote + space + quote + x86_outfile + quote + space + quote + arm_outfile + quote + enforce_silence

            if PRINT_PROGRESS :
                print("(lipo)",LIPO_COMBINE)

            os.system(LIPO_COMBINE)

            CLEANUP = "rm" + space + quote + x86_outfile + quote + space + quote + arm_outfile + quote + enforce_silence

            if PRINT_PROGRESS :
                print("(cleanup)",CLEANUP)

            os.system(CLEANUP)
        
        else :
            COMPILE = INVOKE_CC + space + WARNING_CMD + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + outfile + quote + enforce_silence
            
            if PRINT_PROGRESS :
                print(COMPILE)
            
            os.system(COMPILE)

    else :
        if IF_NOT_DARWIN_COMPILE_BOTH_STATIC_AND_DYNAMIC :
            static_outfile = STATIC_BIN_PREFIX + outfile
            COMPILE_STATIC = INVOKE_CC + space + "-static" + space + WARNING_CMD + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + static_outfile + quote + enforce_silence

            if PRINT_PROGRESS:
                print("(static)",COMPILE_STATIC)
            
            os.system(COMPILE_STATIC)

            dynamic_outfile = DYNAMIC_BIN_PREFIX + outfile
            COMPILE_DYNAMIC = INVOKE_CC + space + WARNING_CMD + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + dynamic_outfile + quote + enforce_silence

            if PRINT_PROGRESS:
                print("(dyanmic)",COMPILE_DYNAMIC)
            
            os.system(COMPILE_DYNAMIC)

        else :
            COMPILE = INVOKE_CC + space + ("-static" * (not IF_NOT_BOTH_THEN_JUST_DYNAMIC)) + space + WARNING_CMD + space + OPTIMIZATION_CMD + space + quote + sources + quote + space + "-o" + space + quote + outfile + quote + enforce_silence

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
