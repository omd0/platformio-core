# Installing PlatformIO Core from omd0 Fork

This repository contains a forked version of PlatformIO Core with modifications to ensure it's installed from the `omd0` fork instead of the official repository.

## Installation Methods

### Method 1: Using the Installation Script

The easiest way to install PlatformIO Core from this fork is to use the provided installation script:

```bash
python3 install_from_fork.py
```

This script will:
- Install PlatformIO Core directly from the `omd0/platformio-core` repository
- Use the `develop` branch by default
- Verify the installation was successful

### Method 2: Manual Installation

You can also install manually using pip:

```bash
python3 -m pip install --upgrade https://github.com/omd0/platformio-core/archive/develop.zip
```

### Method 3: Using PlatformIO's Upgrade Command

After the initial installation, you can use PlatformIO's built-in upgrade command, which has been modified to use this fork:

```bash
pio upgrade --dev
```

## What's Modified

The following files have been modified to ensure installation from the `omd0` fork:

1. **`platformio/commands/upgrade.py`**:
   - `DEVELOP_ZIP_URL` now points to `https://github.com/omd0/platformio-core/archive/develop.zip`
   - `DEVELOP_INIT_SCRIPT_URL` now points to `https://raw.githubusercontent.com/omd0/platformio-core/develop/platformio/__init__.py`

2. **`install_from_fork.py`**:
   - New installation script that ensures installation from the fork

## Verification

To verify that PlatformIO Core was installed from the correct repository:

```bash
pio --version
```

The version should indicate it's from the development branch of the fork.

## Updating

To update PlatformIO Core from the fork:

```bash
pio upgrade --dev
```

This will pull the latest changes from the `develop` branch of the `omd0/platformio-core` repository.

## Troubleshooting

If you encounter issues:

1. **Clear pip cache**:
   ```bash
   python3 -m pip cache purge
   ```

2. **Uninstall existing PlatformIO Core**:
   ```bash
   python3 -m pip uninstall platformio
   ```

3. **Reinstall from fork**:
   ```bash
   python3 install_from_fork.py
   ```

## Notes

- This fork ensures that all installations and upgrades use the `omd0/platformio-core` repository
- The `--dev` flag in `pio upgrade` will always use the fork's develop branch
- Regular `pio upgrade` (without `--dev`) will still use PyPI, but the core dependencies will be managed through the fork 