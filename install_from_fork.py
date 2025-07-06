#!/usr/bin/env python3
"""
Install PlatformIO Core from omd0 fork
This script ensures that PlatformIO Core is installed from the forked repository
"""

import subprocess
import sys
import os

def install_from_fork():
    """Install PlatformIO Core from omd0 fork"""
    
    # Get Python executable path
    python_exe = sys.executable
    
    # Fork repository URL
    fork_url = "https://github.com/omd0/platformio-core/archive/develop.zip"
    
    print("Installing PlatformIO Core from omd0 fork...")
    print(f"Repository: {fork_url}")
    
    try:
        # Install from the fork
        subprocess.run(
            [python_exe, "-m", "pip", "install", "--upgrade", fork_url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Verify installation
        result = subprocess.run(
            [python_exe, "-m", "platformio", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        version = result.stdout.decode().strip()
        print(f"✅ PlatformIO Core successfully installed: {version}")
        print("✅ Installation from omd0 fork completed!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing PlatformIO Core: {e}")
        print(f"Error output: {e.stderr.decode() if e.stderr else 'No error output'}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_from_fork() 