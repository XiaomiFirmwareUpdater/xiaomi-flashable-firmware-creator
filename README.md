## Xiaomi Flashable Firmware Creator

Create flashable firmware zip from MIUI and HyperOS Recovery ROMs!

[![PyPI version](https://badge.fury.io/py/xiaomi-flashable-firmware-creator.svg)](https://pypi.org/project/xiaomi-flashable-firmware-creator/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203-3776AB?style=flat\&labelColor=3776AB\&logo=python\&logoColor=white\&link=https://www.python.org/)](https://www.python.org/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9c1f6cee01b74ef8a2fd0f0c787596a8)](https://www.codacy.com/gh/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator/dashboard?utm_source=github.com\&utm_medium=referral\&utm_content=XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator\&utm_campaign=Badge_Grade)
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](#) <br />
[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=flat\&labelColor=00457C\&logo=PayPal\&logoColor=white\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)
[![Patreon](https://img.shields.io/badge/Patreon-Support-F96854?style=flat\&labelColor=F96854\&logo=Patreon\&logoColor=white\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)
[![Liberapay](https://img.shields.io/badge/Liberapay-Support-F6C915?style=flat\&labelColor=F6C915\&logo=Liberapay\&logoColor=white\&link=https://liberapay.com/yshalsager)](https://liberapay.com/yshalsager)

Xiaomi Flashable Firmware Creator is a tool that generates flashable firmware-update packages from official MIUI and HyperOS ROMS.

It supports creating untouched firmware, non-arb firmware, firmware + vendor flashable zip, and firmware-less ROMs from any local zip file or direct link of the zip file.

### Requirements

This tool requires the following dependencies to be installed on your system:

- **[payload-dumper-go](https://github.com/ssut/payload-dumper-go)**: Used for extracting Android OTA payload files. Install using your system package manager or from releases.
- **[xz](https://tukaani.org/xz/)**: Required for payload decompression.

#### Installing xz

**Linux and macOS (From package manager, recommended)**:

- **Ubuntu/Debian**: `sudo apt install xz-utils`
- **CentOS/RHEL/Fedora**: `sudo yum install xz` or `sudo dnf install xz`
- **Arch Linux**: `sudo pacman -S xz`
- **openSUSE**: `sudo zypper install xz`
- **macOS (Homebrew)**: `brew install xz`
- **macOS (MacPorts)**: `sudo port install xz`

**Windows**:

1. Download the latest XZ Utils for Windows from [tukaani.org/xz/](https://tukaani.org/xz/)
2. Extract the downloaded archive to a directory on your system
3. Add the directory containing `xz.exe` to your system's PATH environment variable

**Verify installation**: Run `xz --version` in your terminal to confirm xz is properly installed.

**Note**: Working on a SSD is highly recommended for performance reasons when processing large payload files, as HDDs can be a bottleneck.

### Installation

You can simply install this tool using [uv](https://docs.astral.sh/uv/).

```shell script
uv install xiaomi_flashable_firmware_creator
```

### CLI Usage

```shell script
xiaomi_flashable_firmware_creator [-h] (-F FIRMWARE | -N NONARB | -L FIRMWARELESS | -V VENDOR) [-o OUTPUT]
```

**Examples:**

*   Creating normal (untouched) firmware:

```shell script
xiaomi_flashable_firmware_creator -F [ROM ZIP]
```

*   Creating non-arb firmware (without anti-rollback):

```shell script
xiaomi_flashable_firmware_creator -N [ROM ZIP]
```

*   Creating firmware-less ROM (stock untouched ROM with just firmware removed):

```shell script
xiaomi_flashable_firmware_creator -L [ROM ZIP]
```

*   Creating firmware + vendor flashable zip:

```shell script
xiaomi_flashable_firmware_creator -V [ROM ZIP]
```

### Using from other Python scripts

```python
from xiaomi_flashable_firmware_creator.firmware_creator import FlashableFirmwareCreator

# initialize firmware creator object with the following parameters:
# input_file: zip file to extract from. It can be a local path or a remote direct url.
# process: Which mode should the tool use. This must be one of "firmware", "nonarb", "firmwareless" or "vendor". (See CLI Usage for more details)
# out_dir: The output directory to store the extracted file in.

firmware_creator = FlashableFirmwareCreator(input_zip, process, output_dir)
# Now, you can either use auto() method to create the new zip file or do stuff at your own using firmware_creator public methods.
new_zip = firmware_creator.auto()
```

## Development

This project uses several tools to streamline the development process:

### mise

[mise](https://mise.jdx.dev/) is used for managing project-level dependencies and environment variables. mise helps ensure consistent development environments across different machines.

To get started with mise:

1. Install mise by following the instructions on the [official website](https://mise.jdx.dev/).
2. Run `mise install` in the project root to set up the development environment.

This file is automatically loaded by mise and allows you to customize your local development environment without modifying the shared configuration files.

### UV

[UV](https://docs.astral.sh/uv/) is used for dependency management and packaging. It provides a clean, version-controlled way to manage project dependencies.

To set up the project with UV:

1. Install UV using mise, or by following the instructions on the [official website](https://docs.astral.sh/uv/getting-started/installation/).
2. Run `uv sync` to install project dependencies.

### Development Tools

For development, this project uses additional tools managed by mise:

- **[payload-dumper-go](https://github.com/ssut/payload-dumper-go)**: Automatically managed by mise when you run `mise install`.
