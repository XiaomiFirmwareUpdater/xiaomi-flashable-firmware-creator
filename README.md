## Xiaomi Flashable Firmware Creator

Create flashable firmware zip from MIUI Recovery ROMs!

[![PyPI version](https://badge.fury.io/py/xiaomi-flashable-firmware-creator.svg)](https://pypi.org/project/xiaomi-flashable-firmware-creator/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203-3776AB?style=flat\&labelColor=3776AB\&logo=python\&logoColor=white\&link=https://www.python.org/)](https://www.python.org/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/9c1f6cee01b74ef8a2fd0f0c787596a8)](https://www.codacy.com/gh/XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator/dashboard?utm_source=github.com\&utm_medium=referral\&utm_content=XiaomiFirmwareUpdater/xiaomi-flashable-firmware-creator\&utm_campaign=Badge_Grade)
[![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](#) <br />
[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=flat\&labelColor=00457C\&logo=PayPal\&logoColor=white\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)
[![Patreon](https://img.shields.io/badge/Patreon-Support-F96854?style=flat\&labelColor=F96854\&logo=Patreon\&logoColor=white\&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)
[![Liberapay](https://img.shields.io/badge/Liberapay-Support-F6C915?style=flat\&labelColor=F6C915\&logo=Liberapay\&logoColor=white\&link=https://liberapay.com/yshalsager)](https://liberapay.com/yshalsager)

Xiaomi Flashable Firmware Creator is a tool that generates flashable firmware-update packages from official MIUI ROMS.

It supports creating untouched firmware, non-arb firmware, firmware + vendor flashable zip, and firmware-less ROMs from any local zip file or direct link of the zip file.

### Installation

You can simply install this tool using Python pip.

```shell script
pip install xiaomi_flashable_firmware_creator
```

### CLI Usage

```shell script
xiaomi_flashable_firmware_creator [-h] (-F FIRMWARE | -N NONARB | -L FIRMWARELESS | -V VENDOR) [-o OUTPUT]
```

**Examples:**

*   Creating normal (untouched) firmware:

```shell script
xiaomi_flashable_firmware_creator -F [MIUI ZIP]
```

*   Creating non-arb firmware (without anti-rollback):

```shell script
xiaomi_flashable_firmware_creator -N [MIUI ZIP]
```

*   Creating firmware-less ROM (stock untouched ROM with just firmware removed):

```shell script
xiaomi_flashable_firmware_creator -L [MIUI ZIP]
```

*   Creating firmware + vendor flashable zip:

```shell script
xiaomi_flashable_firmware_creator -V [MIUI ZIP]
```

### Using from other Python scripts

```python
from xiaomi_flashable_firmware_creator.firmware_creator import FlashableFirmwareCreator

# initialize firmware creator object with the following parameters:
# input_file: zip file to extract from. It can be a local path or a remote direct url.
# process: Which mode should the tool use. This must be one of "firmware", "nonarb", "firmwareless" or "vendor".
# out_dir: The output directory to store the extracted file in.

firmware_creator = FlashableFirmwareCreator(input_zip, process, output_dir)
# Now, you can either use auto() method to create the new zip file or do stuff at your own using firmware_creator public methods.
new_zip = firmware_creator.auto()
```
