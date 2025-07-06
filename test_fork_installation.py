#!/usr/bin/env python3
"""
Test script to verify PlatformIO Core installation from omd0 fork
"""

import subprocess
import sys
import os

def test_fork_installation():
    """Test that PlatformIO Core can be installed from the fork"""
    
    python_exe = sys.executable
    fork_url = "https://github.com/omd0/platformio-core/archive/develop.zip"
    
    print("Testing PlatformIO Core installation from omd0 fork...")
    print(f"Repository: {fork_url}")
    
    try:
        # Test installation (dry run)
        print("Testing pip install command...")
        result = subprocess.run(
            [python_exe, "-m", "pip", "install", "--dry-run", fork_url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("✅ Pip install test passed")
        
        # Test that the URL is accessible
        print("Testing repository accessibility...")
        import urllib.request
        try:
            urllib.request.urlopen(fork_url)
            print("✅ Repository is accessible")
        except Exception as e:
            print(f"❌ Repository accessibility test failed: {e}")
            return False
        
        print("✅ All tests passed! The fork installation should work correctly.")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Test failed: {e}")
        print(f"Error output: {e.stderr.decode() if e.stderr else 'No error output'}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_fork_installation()
    sys.exit(0 if success else 1) 