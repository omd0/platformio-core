# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re

from SCons.Script import COMMAND_LINE_TARGETS  # pylint: disable=import-error


def GenerateCompileCommands(env, target, source):
    """Generate compile_commands.json for clangd compatibility"""
    
    if "compiledb" not in COMMAND_LINE_TARGETS:
        return
    
    compile_commands = []
    
    # Get all source files that were built
    build_files = env.get("PIOBUILDFILES", [])
    
    for build_file in build_files:
        if hasattr(build_file, 'srcnode'):
            src_file = build_file.srcnode().get_abspath()
        else:
            src_file = str(build_file)
            
        # Skip if not a C/C++ file
        if not any(src_file.endswith(ext) for ext in ['.c', '.cpp', '.cc', '.cxx', '.c++']):
            continue
            
        # Determine compiler
        if src_file.endswith('.c'):
            compiler = env.subst("$CC")
            flags = env.subst("$CFLAGS $CCFLAGS $CPPFLAGS")
        else:
            compiler = env.subst("$CXX")
            flags = env.subst("$CXXFLAGS $CCFLAGS $CPPFLAGS")
            
        # Get include paths
        includes = []
        for include_path in env.get("CPPPATH", []):
            includes.append(f"-I{env.subst(str(include_path))}")
            
        # Get defines
        defines = []
        for define in env.get("CPPDEFINES", []):
            if isinstance(define, tuple):
                if len(define) == 2:
                    defines.append(f"-D{define[0]}={define[1]}")
                else:
                    defines.append(f"-D{define[0]}")
            else:
                defines.append(f"-D{define}")
        
        # Filter GCC-specific flags for clangd compatibility
        filtered_flags = filter_gcc_flags_for_clangd(flags, env)
        
        # Build the command
        command_parts = [compiler] + filtered_flags.split() + includes + defines + ["-c", src_file]
        command = " ".join(command_parts)
        
        compile_commands.append({
            "directory": env.subst("$PROJECT_DIR"),
            "file": src_file,
            "command": command
        })
    
    # Write compile_commands.json
    output_path = env.subst("$COMPILATIONDB_PATH")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(compile_commands, f, indent=2)
    
    print(f"Generated {output_path} with {len(compile_commands)} entries")


def filter_gcc_flags_for_clangd(flags_str, env):
    """Filter GCC-specific flags that clangd doesn't understand"""
    
    # Check if clangd flag filtering is enabled (default: True)
    if not env.GetProjectOption("compiledb_clangd_compat", True):
        return flags_str
    
    # GCC flags that clangd doesn't understand
    gcc_only_flags = [
        "-mlongcalls",
        "-fstrict-volatile-bitfields", 
        "-fno-tree-switch-conversion",
        "-fno-jump-tables",
        "-fno-unwind-tables",
        "-fno-asynchronous-unwind-tables",
        "-ffunction-sections",
        "-fdata-sections",
        "-fno-reorder-functions",
        "-fno-reorder-blocks",
        "-fno-reorder-blocks-and-partition",
    ]
    
    # Replace GCC flags with clang equivalents
    flag_replacements = {
        "-mlongcalls": "-mlong-calls",
    }
    
    # Filter flags
    filtered_flags = []
    for flag in flags_str.split():
        if flag in gcc_only_flags:
            continue  # Skip GCC-only flags
        elif flag in flag_replacements:
            filtered_flags.append(flag_replacements[flag])
        else:
            filtered_flags.append(flag)
    
    return " ".join(filtered_flags)


def CompileDbGenerator(env):
    """Add compilation database generation to post-build actions"""
    
    if "compiledb" not in COMMAND_LINE_TARGETS:
        return
        
    # Add our generator as a post-build action
    env.AddPostAction("$PIOMAINPROG", GenerateCompileCommands)


def exists(_):
    return True


def generate(env):
    env.AddMethod(CompileDbGenerator)
    return env 