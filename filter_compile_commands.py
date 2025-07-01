#!/usr/bin/env python3
"""
Filter GCC-specific flags from compile_commands.json for clangd compatibility
Usage: python filter_compile_commands.py [path_to_compile_commands.json]
"""

import json
import sys
import os

def filter_gcc_flags(command_str):
    """Filter GCC-specific flags that clangd doesn't understand"""
    
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
    
    # Split command into parts
    parts = command_str.split()
    filtered_parts = []
    
    for part in parts:
        if part in gcc_only_flags:
            continue  # Skip GCC-only flags
        elif part in flag_replacements:
            filtered_parts.append(flag_replacements[part])
        else:
            filtered_parts.append(part)
    
    return " ".join(filtered_parts)

def main():
    # Get compile_commands.json path
    if len(sys.argv) > 1:
        compile_commands_path = sys.argv[1]
    else:
        compile_commands_path = "compile_commands.json"
    
    if not os.path.exists(compile_commands_path):
        print(f"Error: {compile_commands_path} not found")
        sys.exit(1)
    
    # Load compile_commands.json
    with open(compile_commands_path, 'r') as f:
        compile_commands = json.load(f)
    
    # Filter each compilation unit
    filtered_count = 0
    for unit in compile_commands:
        if "command" in unit:
            original_command = unit["command"]
            filtered_command = filter_gcc_flags(original_command)
            if original_command != filtered_command:
                unit["command"] = filtered_command
                filtered_count += 1
        elif "arguments" in unit:
            original_args = unit["arguments"]
            filtered_args = []
            for arg in original_args:
                if isinstance(arg, str):
                    # Check if this argument is a GCC-only flag
                    gcc_only_flags = [
                        "-mlongcalls", "-fstrict-volatile-bitfields", 
                        "-fno-tree-switch-conversion", "-fno-jump-tables",
                        "-fno-unwind-tables", "-fno-asynchronous-unwind-tables",
                        "-ffunction-sections", "-fdata-sections",
                        "-fno-reorder-functions", "-fno-reorder-blocks",
                        "-fno-reorder-blocks-and-partition",
                    ]
                    if arg in gcc_only_flags:
                        continue  # Skip this flag
                    elif arg == "-mlongcalls":
                        filtered_args.append("-mlong-calls")
                    else:
                        filtered_args.append(arg)
                else:
                    filtered_args.append(arg)
            
            if len(original_args) != len(filtered_args):
                unit["arguments"] = filtered_args
                filtered_count += 1
    
    # Write filtered compile_commands.json
    backup_path = compile_commands_path + ".backup"
    os.rename(compile_commands_path, backup_path)
    
    with open(compile_commands_path, 'w') as f:
        json.dump(compile_commands, f, indent=2)
    
    print(f"✅ Filtered {filtered_count} compilation units")
    print(f"📁 Original file backed up to: {backup_path}")
    print(f"🎯 clangd should now work without GCC flag errors!")

if __name__ == "__main__":
    main() 