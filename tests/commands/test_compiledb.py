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
import tempfile

import pytest

from platformio import fs
from platformio.project.config import ProjectConfig


def test_compiledb_generation(tmpdir):
    """Test that compile_commands.json is generated with proper toolchain paths and includes"""
    
    # Create a simple test project
    project_dir = tmpdir.mkdir("test_compiledb_project")
    
    # Create platformio.ini
    ini_content = """
[env:native]
platform = native
board = native
"""
    with open(os.path.join(project_dir, "platformio.ini"), "w") as f:
        f.write(ini_content)
    
    # Create source file
    src_dir = os.path.join(project_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "main.cpp"), "w") as f:
        f.write("#include <iostream>\nint main() { return 0; }\n")
    
    # Run compiledb command
    from platformio import proc
    result = proc.exec_command(
        ["platformio", "run", "-t", "compiledb"],
        cwd=project_dir
    )
    
    # Check that command succeeded
    assert result["returncode"] == 0, f"Command failed: {result['err']}"
    
    # Check that compile_commands.json was generated
    compile_commands_path = os.path.join(project_dir, "compile_commands.json")
    assert os.path.exists(compile_commands_path), "compile_commands.json was not generated"
    
    # Parse the JSON file
    with open(compile_commands_path, "r") as f:
        compile_commands = json.load(f)
    
    # Validate structure
    assert isinstance(compile_commands, list), "compile_commands.json should be a list"
    assert len(compile_commands) > 0, "compile_commands.json should contain at least one entry"
    
    # Check each compilation unit
    for unit in compile_commands:
        # Validate required fields
        assert "file" in unit, "Each compilation unit must have a 'file' field"
        assert "command" in unit or "arguments" in unit, "Each compilation unit must have 'command' or 'arguments'"
        
        # Check that compiler path is absolute
        if "command" in unit:
            command = unit["command"]
            assert command.startswith("/") or command.startswith('"'), f"Compiler path should be absolute: {command}"
        elif "arguments" in unit:
            arguments = unit["arguments"]
            assert len(arguments) > 0, "Arguments array should not be empty"
            compiler_path = arguments[0]
            assert compiler_path.startswith("/") or compiler_path.startswith('"'), f"Compiler path should be absolute: {compiler_path}"
        
        # Check that include paths are present
        if "command" in unit:
            command = unit["command"]
            assert "-I" in command, "Command should include -I flags for include paths"
        elif "arguments" in unit:
            arguments = unit["arguments"]
            include_flags = [arg for arg in arguments if arg.startswith("-I")]
            assert len(include_flags) > 0, "Arguments should include -I flags for include paths"


def test_compiledb_include_paths_completeness(tmpdir):
    """Test that all necessary include paths are captured in compile_commands.json"""
    
    # Create a test project with custom includes
    project_dir = tmpdir.mkdir("test_compiledb_includes")
    
    # Create platformio.ini with custom build flags
    ini_content = """
[env:native]
platform = native
board = native
build_flags = -I./custom_include -I./another_include
"""
    with open(os.path.join(project_dir, "platformio.ini"), "w") as f:
        f.write(ini_content)
    
    # Create custom include directories
    custom_include = os.path.join(project_dir, "custom_include")
    another_include = os.path.join(project_dir, "another_include")
    os.makedirs(custom_include, exist_ok=True)
    os.makedirs(another_include, exist_ok=True)
    
    # Create source file
    src_dir = os.path.join(project_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "main.cpp"), "w") as f:
        f.write("#include <iostream>\n#include <custom_header.h>\nint main() { return 0; }\n")
    
    # Run compiledb command
    from platformio import proc
    result = proc.exec_command(
        ["platformio", "run", "-t", "compiledb"],
        cwd=project_dir
    )
    
    # Check that command succeeded
    assert result["returncode"] == 0, f"Command failed: {result['err']}"
    
    # Parse compile_commands.json
    compile_commands_path = os.path.join(project_dir, "compile_commands.json")
    with open(compile_commands_path, "r") as f:
        compile_commands = json.load(f)
    
    # Check that custom include paths are present
    for unit in compile_commands:
        if "command" in unit:
            command = unit["command"]
            assert f"-I{custom_include}" in command or f'-I"{custom_include}"' in command, f"Custom include path not found: {command}"
            assert f"-I{another_include}" in command or f'-I"{another_include}"' in command, f"Another include path not found: {command}"
        elif "arguments" in unit:
            arguments = unit["arguments"]
            include_paths = [arg for arg in arguments if arg.startswith("-I")]
            custom_includes = [arg for arg in include_paths if custom_include in arg]
            another_includes = [arg for arg in include_paths if another_include in arg]
            assert len(custom_includes) > 0, f"Custom include path not found in arguments: {arguments}"
            assert len(another_includes) > 0, f"Another include path not found in arguments: {arguments}"


def test_compiledb_clangd_compatibility(tmpdir):
    """Test that generated compile_commands.json is compatible with clangd"""
    
    # Create a test project
    project_dir = tmpdir.mkdir("test_clangd_compatibility")
    
    # Create platformio.ini
    ini_content = """
[env:native]
platform = native
board = native
"""
    with open(os.path.join(project_dir, "platformio.ini"), "w") as f:
        f.write(ini_content)
    
    # Create source file
    src_dir = os.path.join(project_dir, "src")
    os.makedirs(src_dir, exist_ok=True)
    with open(os.path.join(src_dir, "main.cpp"), "w") as f:
        f.write("#include <iostream>\n#include <string>\nint main() { return 0; }\n")
    
    # Run compiledb command
    from platformio import proc
    result = proc.exec_command(
        ["platformio", "run", "-t", "compiledb"],
        cwd=project_dir
    )
    
    # Check that command succeeded
    assert result["returncode"] == 0, f"Command failed: {result['err']}"
    
    # Parse compile_commands.json
    compile_commands_path = os.path.join(project_dir, "compile_commands.json")
    with open(compile_commands_path, "r") as f:
        compile_commands = json.load(f)
    
    # Validate clangd compatibility
    for unit in compile_commands:
        # Check that all paths are absolute
        assert os.path.isabs(unit["file"]), f"File path should be absolute: {unit['file']}"
        
        # Check that compiler path is absolute and exists
        if "command" in unit:
            command_parts = unit["command"].split()
            compiler_path = command_parts[0].strip('"')
            assert os.path.isabs(compiler_path), f"Compiler path should be absolute: {compiler_path}"
            # Note: We can't check if the compiler exists as it might be in a different environment
        elif "arguments" in unit:
            compiler_path = unit["arguments"][0].strip('"')
            assert os.path.isabs(compiler_path), f"Compiler path should be absolute: {compiler_path}"
        
        # Check that include paths are absolute
        if "command" in unit:
            command = unit["command"]
            # Extract include paths from command
            import re
            include_matches = re.findall(r'-I([^"\s]+|"[^"]*")', command)
            for include_path in include_matches:
                include_path = include_path.strip('"')
                assert os.path.isabs(include_path), f"Include path should be absolute: {include_path}"
        elif "arguments" in unit:
            arguments = unit["arguments"]
            include_flags = [arg for arg in arguments if arg.startswith("-I")]
            for flag in include_flags:
                include_path = flag[2:].strip('"')
                assert os.path.isabs(include_path), f"Include path should be absolute: {include_path}" 