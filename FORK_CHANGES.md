# Changes Made to Ensure Installation from omd0 Fork

This document summarizes all the changes made to ensure that PlatformIO Core is installed from the `omd0/platformio-core` fork instead of the official repository.

## Modified Files

### 1. `platformio/commands/upgrade.py`

**Changes:**
- Updated `DEVELOP_ZIP_URL` from `https://github.com/platformio/platformio-core/archive/develop.zip` to `https://github.com/omd0/platformio-core/archive/develop.zip`
- Updated `DEVELOP_INIT_SCRIPT_URL` from `https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/__init__.py` to `https://raw.githubusercontent.com/omd0/platformio-core/develop/platformio/__init__.py`

**Impact:**
- When users run `pio upgrade --dev`, it will now install from the omd0 fork
- Version checking for development builds will use the omd0 fork

### 2. `README.rst`

**Changes:**
- Added a new "Installation from Fork" section
- Included quick installation instructions
- Referenced the detailed installation guide

**Impact:**
- Users will immediately see that this is a forked version
- Clear instructions for installation from the fork

## New Files Created

### 1. `install_from_fork.py`

**Purpose:**
- Dedicated installation script for the fork
- Ensures installation from the correct repository
- Includes verification steps

**Features:**
- Uses the omd0 fork URL
- Verifies installation success
- Provides clear error messages
- Executable script

### 2. `INSTALL_FROM_FORK.md`

**Purpose:**
- Comprehensive installation guide
- Multiple installation methods
- Troubleshooting section
- Explanation of modifications

**Content:**
- Three different installation methods
- What files were modified
- Verification steps
- Troubleshooting guide

### 3. `test_fork_installation.py`

**Purpose:**
- Test script to verify fork installation works
- Checks repository accessibility
- Validates pip installation process

**Features:**
- Dry-run installation test
- URL accessibility check
- Clear success/failure indicators

### 4. `FORK_CHANGES.md`

**Purpose:**
- This document - summary of all changes
- Reference for future modifications
- Documentation of the fork's purpose

## Installation Methods Available

1. **Script Installation**: `python3 install_from_fork.py`
2. **Manual Installation**: `python3 -m pip install --upgrade https://github.com/omd0/platformio-core/archive/develop.zip`
3. **PlatformIO Upgrade**: `pio upgrade --dev` (after initial installation)

## Verification

To verify the installation is from the fork:
```bash
pio --version
```

The version should indicate it's from the development branch of the omd0 fork.

## Testing

Run the test script to verify everything works:
```bash
python3 test_fork_installation.py
```

## Notes

- The fork ensures that all development installations use the omd0 repository
- Regular `pio upgrade` (without `--dev`) still uses PyPI for stable releases
- The core dependencies are managed through the fork
- All installation methods are documented and tested 